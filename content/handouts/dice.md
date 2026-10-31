06 · Plebum Dominium

# Make the three keys

> [!WARNING]
> Never enter seed words on an online computer.

This work starts after Tails has booted with networking set to Disabled, and before any plate is stamped. Five casino dice are required, and every face has to be readable. The work is done three times, for three keys, and the computer is shut down fully between them. A private room, no camera.

## The faces

- 1 is 00. 2 is 01. 3 is 10. 4 is 11.
- 5 and 6 are not bits. Roll those dice again.
- Read the dice left to right, the same way every shake.
- Example: 4, 6, 1, 3, 2 becomes 11, skip the 6, then 00, 10, 01.

## Turn the rolls into 24 words

The dice converter page does the recording, the counting, and the math. It runs offline in the Tails browser. If the page ever says the computer is online, it stops, and the work stops with it.

1. 01 · Boot Tails. Networking Disabled. Copy the checked dice converter page from the data USB to the Desktop.
2. 02 · Open the page in Tor Browser. Enter each face as you roll it. The page keeps faces 1 to 4, skips 5 and 6, and counts the pairs. It stops you at 128.
3. 03 · At 256 bits the page prints 24 words. Word 24 is the check. Do not invent it. Do not “fix” it.
4. 04 · Prove it with the second tool. Two options, pick the easier one. The Ian Coleman page takes the same rolls, no terminal. The Python converter takes the bits from the page, terminal. The 24 words must match. If they differ, stop. Do not pick the prettier list.
5. 05 · Write the 24 words on the grid. Read them back out loud once.
6. 06 · Shut Tails down. Wait until the screen is dark. Then start the next key. Seed 2 is a new set of rolls. Seed 3 is a new set of rolls. Never continue a list from the previous boot.

## The last word is a check

The 24 words are not 24 free choices. The last word carries a short check so a copying mistake is caught before metal is stamped. At least two of these checks are used. If they disagree, the work stops.

- Two tools, same rolls, same 24 words. The page, then the Ian Coleman page or the Python converter. Do not pick the prettier list.
- Let the wallet refuse a bad list. Sparrow or Electrum, networking off, will open a valid list and reject a broken one. If it will not open, do not change a word to force it.
- The math, if it needs to be seen. Twenty-four words are 264 bits. The first 256 are the dice. The last 8 are the check. Only word 24 can change to make that true. It is not chosen. The page appends it after the file has been checked.

## Practice grid

The printed recording grid in the bench sheet PDF still works as the paper backup. Each seed needs about 39 shakes for 256 bits. Count the pairs as you go and stop at 128.

Next, Build the 2-of-3.[← Two boots](/handouts/airgap)[Build the 2-of-3 →](/handouts/sparrow)
