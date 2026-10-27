#!/bin/bash

SERVER=root://cmsio3.rc.ufl.edu:1094

DIRS=(
#"/store/user/dalam/TCPNtuple/Run3/2022EE/EGamma"
#"/store/user/dalam/TCPNtuple/Run3/2022EE/Muon"
#"/store/user/dalam/TCPNtuple/Run3/2024/ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8"
#"/store/user/dalam/TCPNtuple/Run3/2024/Muon0/"
"/store/user/dalam/TCPNtuple/Run3/2024/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/Ntuple_TTToHadronic_2024_miniAODv6_v2"
#"/store/user/dalam/TCPNtuple/Run3/2024/DYto2L-4Jets_Bin-HT-40to70-MLL-4to50_TuneCP5_13p6TeV_madgraphMLM-pythia8/Ntuple_DYJetsToLL_MLL-4to50_HT-40to70_2024_miniAODv6_v2"
)

#for DIR in "${DIRS[@]}"; do
#    echo "========================================"
#    echo "Deleting $DIR"
#
#    LIST=$(mktemp)
#
#    xrdfs $SERVER ls -R "$DIR" > "$LIST"
#
#    # Delete all ROOT files
#    grep '\.root$' "$LIST" | while read f; do
#        echo "rm $f"
#        xrdfs $SERVER rm "$f"
#    done
#
#    # Delete directories from deepest to shallowest
#    grep -v '\.root$' "$LIST" | tac | while read d; do
#        echo "rm $d"
#        xrdfs $SERVER rmdir "$d"
#    done
#
#    # Remove the top-level directory
#    echo "rm $DIR"
#    xrdfs $SERVER rmdir "$DIR"
#
#    rm "$LIST"
#done


MAX_RETRIES=2
DELAY=2

delete_file()
{
    local file="$1"

    for ((i=1; i<=MAX_RETRIES; i++)); do

        echo "rm $file"

        output=$(xrdfs "$SERVER" rm "$file" 2>&1)
        status=$?

        if [[ $status -eq 0 ]]; then
            return 0
        fi

        echo "$output"

        if (( i < MAX_RETRIES )); then
            echo "Retrying in ${DELAY}s..."
            sleep "$DELAY"
            DELAY=$((DELAY * 2))
        fi
    done

    echo "FAILED: $file"
    return 1
}


for DIR in "${DIRS[@]}"; do

    echo "========================================"
    echo "Deleting $DIR"
    echo "========================================"

    LIST=$(mktemp)

    if ! xrdfs "$SERVER" ls -R "$DIR" > "$LIST"; then
        echo "ERROR: Could not list $DIR"
        rm -f "$LIST"
        continue
    fi

    #
    # Delete files.
    #
    echo "Deleting files..."

    grep -E '\.(root|tar|tar\.gz|gz|log)$' "$LIST" |
    while IFS= read -r file; do

        # Reset retry delay for each file
        DELAY=2

        delete_file "$file"

        # Don't hammer the DFS server
        sleep 1

    done


    #
    # Wait before directory operations
    #
    echo "Waiting before removing directories..."
    sleep 5


    #
    # Remove directories, deepest first
    #
    echo "Removing directories..."

    grep -vE '\.(root|tar|tar\.gz|gz|log)$' "$LIST" |
    tac |
    while IFS= read -r dir; do

        [[ -z "$dir" ]] && continue
        [[ "$dir" == "$DIR" ]] && continue

        echo "rmdir $dir"

        xrdfs "$SERVER" rmdir "$dir"

        sleep 1
    done


    #
    # Remove top-level directory
    #
    echo "Removing top-level directory..."

    if xrdfs "$SERVER" rmdir "$DIR"; then
        echo "Successfully removed $DIR"
    else
        echo "Could not remove $DIR"
    fi

    rm -f "$LIST"

done
