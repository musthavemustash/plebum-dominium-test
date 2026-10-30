11 · Plebum Dominium

# Hide the wallet map

The map can watch the money, but it cannot spend. The plates are not the map, and the map is not a seed. Anyone who can read it can see the balance, so it never sits around as plain text.

Files used: Tails 7.15.1 or later 7.x (verified).

## What is required

- The wallet map on the data USB, called map.txt only while you work.
- The descriptor tool page from the kit. Checked before it's copied.
- Tails, networking Disabled. Not the everyday computer.
- EFF word list generated passphrase.

## Make a passphrase with dice

Roll five dice at once. Read the faces left to right and look that five digit number up in the EFF Long Wordlist. Write down the word. Repeat to at least six words. Six words give about 77 bits. Example: panoramic nectar precut smith banana handclap.

Use the EFF word list as a text download from the kit, or the Diceware mapper from a saved copy, in an offline Tails session, networking Disabled, never in an everyday browser.

Write the words on paper, in two separate places. Never stamp a passphrase on a plate. Never keep the passphrase paper with the plate, the map, or the USBs. Use the passphrase for one purpose only. It is not a seed, and it is not the decoy passphrase.

Do not confuse the two dice methods. Seed keys use faces 1 to 4 kept, 5 and 6 rerolled, bits build 24 words. Passphrase words use faces 1 to 6 all kept, no rerolls, five dice give one word. A passphrase word is never a seed word.

## Step 1 · Boot Tails. Copy the tool and the map.

::fig encryption/encrypt-setup

Boot Tails, networking Disabled. Copy the tool page and map.txt to the Desktop.

## Step 2 · Open the tool. Encrypt the map.

::fig encryption/encrypt-run

Open the tool page in Tor Browser. The page checks the computer is offline before it starts. Choose Encrypt a map. Drop map.txt anywhere on the page, or paste the text. Choose a passphrase and enter it twice. The words never appear, one dot per character. Review the map, then Encrypt. Download map.txt.asc.

## Step 3 · Copy the locked file. Delete the plain one.

::fig encryption/encrypt-distribute

Copy map.txt.asc to two USB drives. Delete map.txt from the Desktop and the USB. Empty the trash.

## Step 4 · Write the passphrase on paper. Twice.

::fig encryption/passphrase-paper

Two copies, two separate places. This paper is a single point of failure for every encrypted copy of the map. Treat it like a plate.

## Step 5 · Prove it opens. Check the first address.

::fig encryption/encrypt-verify

On a later offline boot, open the tool page again. Choose Decrypt a map. Paste the armored text through the END PGP MESSAGE line. Enter the passphrase once. The restored map must match, and the first address must match what you wrote down. If a plain copy was ever made, encrypt it again, then delete the plain one.

If the passphrase is lost, the coins aren't gone, as long as all three plates still exist. Three seeds rebuild the map exactly. Two seeds cannot. Write the path m/48'/0'/0'/2' on the inheritance sheet. It is not a secret.

## Stop if

- The tool page says the computer is online: stop. Do not type the passphrase.
- You want the xpubs on paper "just in case": that's a leak. Stop.
- You want to invent a homemade cipher: stop. Use the tool.
- The passphrase is a seed or is stamped on a plate: start over with a different one.

Next, If I am gone.[← Metal and the map](/handouts/titanium)[If I am gone →](/handouts/inheritance)
