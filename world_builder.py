from room import Room
from puzzle import Puzzle
from weapon import Weapon
from consumable import Consumable
from misc import Misc

class WorldBuilder:
    def __init__(self):
        self.rooms = {}

    def build(self):
        """
            Creates all rooms, connects them with exits,
            places items/puzzles/monsters, and returns the starting room.
        :return: The starting room.
        """

        # build rooms
        a0 = Room(
            "Boot Sector",
            """
            +----------------------------- BOOT SECTOR ------------------------------+
                System booting...

                    [ Initialising user shell ]
                    [ Loading visual layer    ]
                    [ Syncing input streams   ]

                A plain-looking room forms around you, 
                like the world is still loading.
                Bits of code fall from the ceiling. 
                Something small glints on the floor.

                Exits: EAST -> Lost Cache, SOUTH -> Glitch Pit
            +------------------------------------------------------------------------+
            """
        )

        a1 = Room(
            "Lost Cache",
            """
            +------------------------- LOST CACHE -----------------------------------+
                Piles of old memory blocks are stacked everywhere. 
                Some flicker, some don't load at all.

                    < Rebuilding item data ... 12% >
                    < Warning: corrupted fragment >

                A small terminal hums quietly. 
                Something useful might be buried here.

                Exits: WEST -> Boot Sector
            +------------------------------------------------------------------------+
            """
        )

        b0 = Room(
            "Glitch Pit",
            """
            +-------------------------- GLITCH PIT ----------------------------------+
                The ground seems unreliable here.  
                Tiles appear late, and some just blink in and out of existence.

                    !! Terrain error: mesh failed to load !!
                    A twitching, half-rendered monster notices you.

                This area feels dangerous.

                Exits: NORTH -> Boot Sector, EAST -> Data Well, WEST -> Dead Pixels
            +------------------------------------------------------------------------+
            """
        )

        b1 = Room(
            "Data Well",
            """
            +--------------------------- DATA WELL ----------------------------------+
                A column of falling numbers spills from the ceiling like a waterfall.
                Binary streams flow along the floor.

                    010101... 011001... 010110...
                    A terminal nearby flashes: "LOG AVAILABLE"

                A puzzle seems to be woven into the data flow itself.

                Exits: WEST -> Glitch Pit, SOUTH -> Corrupted Arsenal
            +------------------------------------------------------------------------+
            """
        )

        b2 = Room(
            "Corrupted Arsenal",
            """
            +------------------------- CORRUPTED ARSENAL ----------------------------+
                Rusty-looking digital weapon models float in the air, 
                but many fail to render correctly.

                   [ locked slot       ]
                   [ missing texture   ]
                   [ weapon_error_4F   ]

                A larger puzzle device sparks occasionally.
                Your backpack system activates when entering this place.

                Exits: NORTH -> Data Well, SOUTH -> Gatekeeper Node
            +------------------------------------------------------------------------+
            """
        )

        b3 = Room(
            "Dead Pixels",
            """
            +------------------------------ DEAD PIXELS -----------------------------+
                The walls here have broken into scattered pixel noise.  
                                                       
                           . . .     . # .   . . # # .    . # . .               
                             #   . # .   . .   # .   #     .    .               
                           .   # # .   .   # #     .      # . . .               
                                                                    
                Black and white squares flicker without a pattern.    
                It feels like an unfinished part of the mysterious labyrinth.         
                                                                    
                Exits: EAST -> Glitch Pit                              
            +-----------------------------------------------------------------------+

            """
        )

        c0 = Room(
            "Phantom Node",
            """
            +--------------------------- PHANTOM NODE -------------------------------+
                This room shouldn't exist...  
                Its walls are only half-there, fading in and out like a memory.

                   You feel watched.
                   A strange object hovers silently.

                A doorway flickers in and out of existence, revealing a direct
                link to a powerful presence deeper in the system...

                Exits: SOUTH -> Gatekeeper Node
            +------------------------------------------------------------------------+
            """
        )

        c2 = Room(
            "Gatekeeper Node",
            """
            +-------------------------- GATEKEEPER NODE -----------------------------+
                A massive corrupted guardian blocks the path ahead.
                It flickers between frames, unfinished and unstable.

                   ACCESS DENIED: kernel key required
                   The creature roars and the whole room shudders.

                This fight is unavoidable.

                Exits: NORTH -> Corrupted Arsenal, SOUTH -> Fractured Archive (locked)
            +------------------------------------------------------------------------+
            """
        )

        d0 = Room(
            "Fractured Archive",
            """
            +------------------------- FRACTURED ARCHIVE ----------------------------+
                Broken bits of past events float around like ghosts.
                Some logs replay wrong. Others don't load at all.

                   [ log_04: missing timestamp ]
                   [ memory chunk corrupted    ]

                A console sits in the centre, but it needs a decryption item.

                Exits: NORTH -> Gatekeeper Node, EAST -> Obsolete Hub
            +------------------------------------------------------------------------+
            """
        )

        d1 = Room(
            "Obsolete Hub",
            """
            +--------------------------- OBSOLETE HUB -------------------------------+
                This room feels outdated. Old system functions lie everywhere,  
                half-functional and flickering.

                   < deprecated_module >
                   < legacy API called >
                   < unsupported format >

                A giant puzzle dominates the middle of the room.

                Exits: WEST -> Fractured Archive, NORTH -> System Kernel
            +------------------------------------------------------------------------+
            """
        )

        d2 = Room(
            "System Kernel",
            """
            +---------------------------- SYSTEM KERNEL -----------------------------+
                Everything is suddenly calm.  
                The glitches are gone. The room is clean and bright.

                   You hold the kernel key.
                   A door of pure white light waits for you.

                This is the exit.

                Exits: none
            +------------------------------------------------------------------------+
            """
        )

        self.rooms = {"a0": a0, "a1": a1, "b0": b0, "b1": b1, "b2": b2, "b3": b3,
                      "c0": c0, "c2": c2, "d0": d0, "d1": d1, "d2": d2
                      }

        self.link_rooms()
        self.place_items()
        self.place_puzzles()
        self.place_monsters()

    def link_rooms(self):
        """
            Creates directional exits between rooms.
        :return: None
        """
        # Boot Sector (spawn)
        self.rooms["a0"].set_exit("east", self.rooms["a1"])
        self.rooms["a0"].set_exit("south", self.rooms["b0"])

        # Lost Cache
        self.rooms["a1"].set_exit("west", self.rooms["a0"])

        # Glitch Pit
        self.rooms["b0"].set_exit("north", self.rooms["a0"])
        self.rooms["b0"].set_exit("east", self.rooms["b1"])
        self.rooms["b0"].set_exit("west", self.rooms["b3"])  # dead-end branch

        # Dead Pixels
        self.rooms["b3"].set_exit("east", self.rooms["b0"])  # only way back

        # Data Well
        self.rooms["b1"].set_exit("west", self.rooms["b0"])
        self.rooms["b1"].set_exit("south", self.rooms["b2"])

        # Corrupted Arsenal
        self.rooms["b2"].set_exit("north", self.rooms["b1"])
        self.rooms["b2"].set_exit("south", self.rooms["c2"])  # boss path

        # Phantom Node (secret room) - unlocked separately
        self.rooms["c0"].set_exit("south", self.rooms["c2"])  # secret shortcut back to maze

        # Gatekeeper Node (boss)
        self.rooms["c2"].set_exit("north", self.rooms["b2"])
        self.rooms["c2"].set_exit("south", self.rooms["d0"])

        # Fractured Archive
        self.rooms["d0"].set_exit("north", self.rooms["c2"])
        self.rooms["d0"].set_exit("east", self.rooms["d1"])

        # Obsolete Hub
        self.rooms["d1"].set_exit("west", self.rooms["d0"])
        self.rooms["d1"].set_exit("north", self.rooms["d2"])

        # System Kernel is endgame (no exits)

    def place_items(self):
        """
            Place Item objects into chosen rooms.
        :return: None
        """
        # -------------------- A-TIER ITEMS --------------------
        fragmented_blade = Weapon(
            "Fragmented Blade",
            "A weak blade formed from unstable data shards.",
            damage=3,
            weight=1
        )
        self.rooms["a0"].add_item(fragmented_blade)

        hidden_packet = Misc(
            "Hidden Packet",
            "A strange block of corrupted data. It seems to resonate with unseen doorways.",
            misc_id="unlock_c0"
        )
        self.rooms["a1"].add_item(hidden_packet)

        # -------------------- B-TIER ITEMS --------------------
        scan_module = Misc(
            "Scan Module",
            "Allows you to read corrupted logs and system terminals.",
            misc_id="scan"
        )
        data_chip = Misc(
            "Data Chip",
            "A broken memory chip containing fragments of lore.",
            misc_id="lore"
        )
        self.rooms["b1"].add_item(scan_module)
        self.rooms["b1"].add_item(data_chip)

        backpack_upgrade = Misc(
            "Backpack Upgrade",
            "Upgrades your inventory capacity using adaptive memory compression.",
            misc_id="bag_upgrade"
        )
        kernels_edge = Weapon(
            "Kernel's Edge",
            "A powerful blade formed from unstable data.",
            damage=7,
            weight=2
        )
        self.rooms["b2"].add_item(backpack_upgrade)
        self.rooms["b2"].add_item(kernels_edge)

        # -------------------- C-TIER ITEMS --------------------
        ghost_fragment = Misc(
            "Ghost Fragment",
            "A rare unstable data fragment pulsing faintly.",
            misc_id="ghost"
        )
        signal_tuner = Consumable(
            "Signal Tuner",
            "A device that stabilises your attacks temporarily.",
            heal=0
        )
        self.rooms["c0"].add_item(ghost_fragment)
        self.rooms["c0"].add_item(signal_tuner)

        # -------------------- D-TIER ITEMS --------------------
        decryptor = Misc(
            "Decryptor",
            "Required to operate the final console in the Obsolete Hub.",
            misc_id="decrypt"
        )
        fractured_log = Misc(
            "Fractured Log",
            "A corrupted log showing pieces of the system's history.",
            misc_id="lore2"
        )
        self.rooms["d0"].add_item(decryptor)
        self.rooms["d0"].add_item(fractured_log)

    def place_puzzles(self):
        """
            Assign Puzzle objects to chosen rooms.
        :return: None
        """
        # -------------------- A1 – LOST CACHE --------------------
        puzzle_a1 = Puzzle(
            prompt="Reconstruct the missing byte: 101_01 → what number completes the sequence?",
            solution="0",
            reward="unlock_hidden_packet"
        )
        self.rooms["a1"].puzzle = puzzle_a1

        # -------------------- B1 – DATA WELL --------------------
        puzzle_b1 = Puzzle(
            prompt="Decode the binary sequence: 0100 0001 = ? (ASCII)",
            solution="A",
            reward=None  # reward is using scan_module effectively
        )
        self.rooms["b1"].puzzle = puzzle_b1

        # -------------------- B2 – CORRUPTED ARSENAL --------------------
        puzzle_b2 = Puzzle(
            prompt="Repair the corrupted kernel header: K_RN_L → fill the missing letters.",
            solution="KERNEL",    # accepting "KERNEL" in game logic is easy too
            reward="unlock_kernels_edge"  # Game will interpret this as unlocking the weapon
        )
        self.rooms["b2"].puzzle = puzzle_b2

        # -------------------- C0 – PHANTOM NODE (SECRET) --------------------
        puzzle_c0 = Puzzle(
            prompt="A whisper: 'What remains when memory fades?'",
            solution="echo",
            reward=None  # optional: can spawn lore item if you want
        )
        self.rooms["c0"].puzzle = puzzle_c0

        # -------------------- D1 – OBSOLETE HUB (FINAL PUZZLE) --------------------
        puzzle_d1 = Puzzle(
            prompt="Enter the decryption key: XOR(7, 12) = ?",
            solution="11",
            reward="unlock_exit"  # unlocks passage to System Kernel
        )
        self.rooms["d1"].puzzle = puzzle_d1

    def place_monsters(self):
        """
            Assign Monster objects to chosen rooms.
        :return: None
        """


