from room import Room
from puzzle import Puzzle
from monster import Monster
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
+------------------------------------------------------------------------+

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
            """,
            locked = True
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

        return a0

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
        # a items
        fragmented_blade = Weapon(
            "fragmented_blade",
            "A weak blade formed from unstable data shards.",
            damage=3,
            weight=1
        )
        health_module = Consumable(
            "health_module",
            "A compact utility that repairs corrupted user data. Activating it restores a portion of your health.",
            weight=16,
            heal=2
        )
        self.rooms["a0"].add_item(health_module)
        self.rooms["a0"].add_item(fragmented_blade)

        # b items
        first_corruption = Misc(
            "first_corruption.log",
            "A corrupted monster's log containing forgotten memories.",
            weight=4,
            misc_id="lore2"
        )

        log_module = Misc(
            "log_module",
            "Allows you to read corrupted logs and system terminals.",
            weight=8,
            misc_id="log"
        )
        data_chip = Misc(
            "data_chip.log",
            "A broken memory chip containing a fragment of origins.",
            weight=4,
            misc_id="lore1"
        )
        self.rooms["b1"].add_item(log_module)
        self.rooms["b1"].add_item(data_chip)

        backpack_upgrade = Misc(
            "backpack_upgrade",
            "Upgrades your inventory capacity using adaptive memory compression.",
            weight=8,
            misc_id="bag_upgrade"
        )
        kernels_edge = Weapon(
            "kernels_edge",
            "A powerful blade formed from unstable data.",
            damage=7,
            weight=64
        )
        self.rooms["b2"].add_item(backpack_upgrade)
        self.rooms["b2"].add_item(kernels_edge)

        # c items
        signal_tuner = Consumable(
            "signal_tuner",
            "A device that stabilises your attacks temporarily.",
            weight="16",
            heal=0
        )
        self.rooms["c0"].add_item(signal_tuner)

        # -------------------- D-TIER ITEMS --------------------
        decryptor = Misc(
            "decrypter",
            "Required to operate the final console in the Obsolete Hub.",
            weight=8,
            misc_id="decrypt"
        )
        fractured = Misc(
            "fractured.log",
            "A corrupted log showing pieces of the system's history.",
            weight=4,
            misc_id="lore4"
        )
        self.rooms["d0"].add_item(decryptor)
        self.rooms["d0"].add_item(fractured)

    def place_puzzles(self):
        """
            Assign Puzzle objects to chosen rooms.
        :return: None
        """
        # -------------------- A1 – LOST CACHE --------------------
        puzzle_a1 = Puzzle(
            name="Reconstruction",
            prompt="Reconstruct the missing byte: 101_01 → what number completes the sequence?",
            solution="0",
            reward="unlock_hidden_packet"
        )
        self.rooms["a1"].puzzle = puzzle_a1

        # -------------------- B1 – DATA WELL --------------------
        puzzle_b1 = Puzzle(
            name="Binary Code",
            prompt="Decode the binary sequence: 0100 0001 = ? (ASCII)",
            solution="A",
            reward=None  # reward is using scan_module effectively
        )
        self.rooms["b1"].puzzle = puzzle_b1

        # -------------------- B2 – CORRUPTED ARSENAL --------------------
        puzzle_b2 = Puzzle(
            name="Kernel Repair",
            prompt="Repair the corrupted kernel header: K_RN_L → fill the missing letters.",
            solution="KERNEL",    # accepting "KERNEL" in game logic is easy too
            reward="unlock_kernels_edge"  # Game will interpret this as unlocking the weapon
        )
        self.rooms["b2"].puzzle = puzzle_b2

        # -------------------- C0 – PHANTOM NODE (SECRET) --------------------
        puzzle_c0 = Puzzle(
            name="Faded Data",
            prompt="A whisper: 'What remains when memory fades?'",
            solution="echo",
            reward=None  # optional: can spawn lore item if you want
        )
        self.rooms["c0"].puzzle = puzzle_c0

        # -------------------- D1 – OBSOLETE HUB (FINAL PUZZLE) --------------------
        puzzle_d1 = Puzzle(
            name="Unlocking the Door",
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
        glitch_beast = Monster(
            name="glitch_beast",
            description="A twitching creature made of broken meshes and flickering polygons.",
            hp=6,
            max_hp=6,
            attack_power=2,
            reward=Misc(
                "data_key",
                "A key to the Data Well dropped by the glitch_beast.",
                weight=8,
                misc_id="data_key"
            ),
            blocks_exit="east"
        )
        self.rooms["b0"].add_monster(glitch_beast)

        data_wraith = Monster(
            name="data_wraith",
            description="A humanoid shape made of streaming binary. Its form shifts unpredictably.",
            hp=10,
            max_hp=10,
            attack_power=3,
            reward=None
        )
        self.rooms["b1"].add_monster(data_wraith)

        corrupted_drone = Monster(
            name="corrupted_drone",
            description="A floating defense unit, its casing fractured and emitting sparks.",
            hp=14,
            max_hp=14,
            attack_power=4,
            reward=None
        )
        self.rooms["b2"].add_monster(corrupted_drone)

        # -------------------- SECRET ROOM MONSTER --------------------

        echo_shade = Monster(
            name="echo_shade",
            description="A faint silhouette, like a shadow of code that never fully loads.",
            hp=12,
            max_hp=12,
            attack_power=4,
            reward=None
        )
        self.rooms["c0"].add_monster(echo_shade)

        # -------------------- BOSS MONSTER --------------------

        gatekeeper = Monster(
            name="gatekeeper",
            description=(
                "A massive corrupted guardian flickering between frames. It guards the kernel path."
            ),
            hp=25,
            max_hp=25,
            attack_power=6,
            reward=Misc("kernel_key", "A critical system key dropped by the Gatekeeper.", weight="1.5", misc_id="kernel")
        )
        self.rooms["c2"].add_monster(gatekeeper)

        # -------------------- ARCHIVE MONSTER --------------------

        memory_phantom = Monster(
            name="memory_phantom",
            description="A ghost formed from corrupted logs and broken memories.",
            hp=15,
            max_hp=15,
            attack_power=5,
            reward=None
        )
        self.rooms["d0"].add_monster(memory_phantom)

