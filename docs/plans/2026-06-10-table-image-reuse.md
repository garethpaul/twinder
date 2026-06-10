# Saved-Profile Table Image Reuse

Status: Completed

## Goal

Prevent saved-profile rows from crashing on malformed image data or showing
an image downloaded for a cell's previous row after that cell is reused.

## Changes

- Clear the image view whenever a saved-profile cell is configured.
- Validate remote image URLs and decoded image data before use.
- Confirm the cell still represents the requested index path before assigning
  an asynchronous image result.
- Add static contracts for the URL, decoded-image, and reuse identity guards.

## Verification

- Run `make check`.
- Remove the current-index-path comparison and confirm the static contract
  checker fails before restoring it.
