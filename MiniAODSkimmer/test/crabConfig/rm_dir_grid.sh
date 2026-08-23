#!/bin/bash

SERVER=root://cmsio2.rc.ufl.edu:1094

DIRS=(
"/store/user/dalam/TCPNtuple/Run3/2022EE/EGamma"
"/store/user/dalam/TCPNtuple/Run3/2022EE/Muon"
"/store/user/dalam/TCPNtuple/Run3/2022EE/MuonEG"
)

for DIR in "${DIRS[@]}"; do
    echo "========================================"
    echo "Deleting $DIR"

    LIST=$(mktemp)

    xrdfs $SERVER ls -R "$DIR" > "$LIST"

    # Delete all ROOT files
    grep '\.root$' "$LIST" | while read f; do
        echo "rm $f"
        xrdfs $SERVER rm "$f"
    done

    # Delete directories from deepest to shallowest
    grep -v '\.root$' "$LIST" | tac | while read d; do
        echo "rmdir $d"
        xrdfs $SERVER rmdir "$d"
    done

    # Remove the top-level directory
    echo "rmdir $DIR"
    xrdfs $SERVER rmdir "$DIR"

    rm "$LIST"
done