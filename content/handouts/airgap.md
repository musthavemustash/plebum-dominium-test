04 · Plebum Dominium

# Two boots

One computer, used twice. The first boot watches the wallet and broadcasts finished payments. It never holds a seed. The second boot is the Tails USB: networking off, exactly one seed, then a full shutdown. The seed lives in memory only. Shutdown wipes it.

Files used: Tails 7.15.1 or later 7.x (verified).

::fig airgap/two-boots

## What "airgapped" means here

Yes:

- Networking Disabled on the Tails welcome screen, before the desktop.
- Files cross on the data USB: payment files, the map, checked programs.
- The online computer stays watch-only.

Not airgapped:

- Turning networking off after Sparrow opened.
- Unplugging a disk that was online yesterday.
- A photo of a seed. A password manager, printer, or cloud note as backup.

## Prepare the two USBs

::fig airgap/two-usbs

Download Tails only from the official site. Check the signature and checksum before writing. Write it with the official installer, label it TAILS. Do not create Persistent Storage. Skip the passphrase. The data USB gets only files that already passed the checks.

## Every offline session

1. Boot the Tails drive. Networking Disabled. Don't unlock Persistent Storage.
2. Copy only the file that session needs from the data USB.
3. Do the work: convert dice, restore one seed, sign one file, or export the map.
4. Copy the result back to the data USB. Shut down fully. Dark screen before the drive comes out.

## Stop if

- Two seeds in one session: never.
- Networking turns on while a seed is in memory: that session is burned.
- Tails offers Persistent Storage: don't create it, don't unlock it.

<!-- TEST MOCKUP: dedicated-laptop section, exploratory, not on live -->
## The dedicated laptop (optional, stronger)

A second computer takes the place of the second boot. It is an old laptop, bought used, that never touches a network.

Buy used. A ThinkPad X230 or anything similar, around $200, with a Wi-Fi card that comes out. Wipe the drive on arrival and leave it blank. Nothing from its old life stays.

Open the case and pull the Wi-Fi card. If Bluetooth shares the card, it goes with it. Never plug in Ethernet. This is the whole point: with no network hardware, no screen setting can put it online.

The Tails USB boots on this laptop exactly as this sheet describes. Networking is still set to Disabled on the welcome screen. The data USB still carries files both ways. The daily computer never reboots. It stays online and watch-only, always.

A hard drive remembers, so seed words never touch the laptop's disk. They live in memory, on the grid, then on the plates. Tails forgetting everything at shutdown still applies.

If a network cable ever touches the laptop, wipe it again before it holds a seed.

The Tails file is still checked before it is written. The data USB still carries only checked files. The stick remains the only wire.

Next, Make the three keys.[← Check the files](/handouts/verify)[Make the three keys →](/handouts/dice)
