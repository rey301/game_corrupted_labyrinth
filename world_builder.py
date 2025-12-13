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
            "boot_sector",
            """
            
                                    | BOOT SECTOR |

                            System booting...
                            [ Initialising user shell ]
                            [ Loading visual layer    ]
                            [ Syncing input streams   ]
    
        A plain-looking room forms around you, like the world is still loading.
        Bits of code fall from the ceiling. Something small glints on the floor.

    Exits: NORTH -> Lost Cache, SOUTH -> Glitch Pit
            """
        )

        a1 = Room(
            "lost_cache",
            """
            
                                    | LOST CACHE |

                            < Rebuilding item data ... 12% >
                            < Warning: corrupted fragment >
        
        Piles of old memory blocks are stacked everywhere. Some flicker, some 
        don't load at all. A small terminal hums quietly. 
        Something useful might be buried here.

    Exits: SOUTH -> Boot Sector
            """
        )

        b0 = Room(
            "glitch_pit",
            """
            
                                    | GLITCH PIT |
                                    
                          ..+....>:>:..///...;;....;_///..<
                          ||.,,,;....;_///..<---------------
                            
                        !! Terrain error: mesh failed to load !!
                     A twitching, half-rendered monster notices you.
                          
        The ground seems unreliable here. Tiles appear late, and some just 
        blink in and out of existence. This area feels dangerous.

    Exits: NORTH -> Boot Sector, EAST -> Data Well, WEST -> Dead Pixels
            """
        )

        b1 = Room(
            "data_well",
            """
                                    | DATA WELL |
        A column of falling numbers spills from the ceiling like a waterfall.
        Binary streams flow along the floor.
    
            010101... 011001... 010110...
            A terminal nearby flashes: "LOG AVAILABLE"
    
        A puzzle seems to be woven into the data flow itself.

    Exits: WEST -> Glitch Pit, SOUTH -> Corrupted Arsenal
            """
        )

        b2 = Room(
            "corrupted_arsenal",
            """
                          | CORRUPTED ARSENAL |
    Rusty-looking digital weapon models float in the air, 
    but many fail to render correctly.

       [ locked slot       ]
       [ missing texture   ]
       [ weapon_error_4F   ]

    A larger puzzle device sparks occasionally.
    Your backpack system activates when entering this place.

    Exits: NORTH -> Data Well, EAST -> Gatekeeper Node
+------------------------------------------------------------------------+
            """
        )

        b3 = Room(
            "dead_pixels",
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
            "phantom_node",
            """
+--------------------------- PHANTOM NODE -------------------------------+
    This room shouldn't exist...  
    Its walls are only half-there, fading in and out like a memory.

       You feel watched.
       A strange object hovers silently.

    A doorway flickers in and out of existence, revealing a direct
    link to a powerful presence deeper in the system...

    Exits: SOUTH -> Gatekeeper Node, WEST -> Boot Sector
+------------------------------------------------------------------------+
            """,
            locked = True
        )

        c2 = Room(
            "gatekeeper_node",
            """
+-------------------------- GATEKEEPER NODE -----------------------------+
    A massive corrupted guardian blocks the path ahead.
    It flickers between frames, unfinished and unstable.

       ACCESS DENIED: kernel key required
       The creature roars and the whole room shudders.

    This fight is unavoidable.

    Exits: WEST -> Corrupted Arsenal, EAST -> Fractured Archive
+------------------------------------------------------------------------+
            """
        )

        d0 = Room(
            "fractured_archive",
            """
+------------------------- FRACTURED ARCHIVE ----------------------------+
    Broken bits of past events float around like ghosts.
    Some logs replay wrong. Others don't load at all.

       [ log_04: missing timestamp ]
       [ memory chunk corrupted    ]

    A console sits in the centre, but it needs a decryption item.

    Exits: WEST -> Gatekeeper Node, NORTH -> Obsolete Hub
+------------------------------------------------------------------------+
            """
        )

        d1 = Room(
            "obsolete_hub",
            """
+--------------------------- OBSOLETE HUB -------------------------------+
    This room feels outdated. Old system functions lie everywhere,  
    half-functional and flickering.

       < deprecated_module >
       < legacy API called >
       < unsupported format >

    A giant puzzle dominates the middle of the room.

    Exits: SOUTH -> Fractured Archive, NORTH -> System Kernel
+------------------------------------------------------------------------+
            """
        )

        d2 = Room(
            "system_kernel",
            """
+---------------------------- SYSTEM KERNEL -----------------------------+
Everything is suddenly calm.  
The glitches are gone. The room is clean and bright.

   You hold the kernel key.
   A door of pure white light waits for you.

The path leads you back, back to the real world.

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
        self.rooms["a0"].set_exit("north", self.rooms["a1"])
        self.rooms["a0"].set_exit("south", self.rooms["b0"])
        self.rooms["a0"].set_exit("east", self.rooms["c0"]) # phantom node
        self.rooms["a0"].lock_exit("east", "unlock_c0")

        # Lost Cache
        self.rooms["a1"].set_exit("south", self.rooms["a0"])

        # Glitch Pit
        self.rooms["b0"].set_exit("north", self.rooms["a0"])
        self.rooms["b0"].set_exit("east", self.rooms["b1"])
        self.rooms["b0"].lock_exit("east", "d4t4") # lock the door to data well
        self.rooms["b0"].set_exit("west", self.rooms["b3"])  # dead-end branch

        # Dead Pixels
        self.rooms["b3"].set_exit("east", self.rooms["b0"])  # only way back

        # Data Well
        self.rooms["b1"].set_exit("west", self.rooms["b0"])
        self.rooms["b1"].set_exit("south", self.rooms["b2"])

        # Corrupted Arsenal
        self.rooms["b2"].set_exit("north", self.rooms["b1"])
        self.rooms["b2"].set_exit("east", self.rooms["c2"])  # boss path

        # Phantom Node (secret room) - unlocked separately
        self.rooms["c0"].set_exit("south", self.rooms["c2"]) # secret shortcut to gatekeeper
        self.rooms["c0"].set_exit("west", self.rooms["a0"]) # boot sector (spawn)

        # Gatekeeper Node (boss)
        self.rooms["c2"].set_exit("west", self.rooms["b2"])
        self.rooms["c2"].set_exit("east", self.rooms["d0"])
        self.rooms["b0"].lock_exit("east", "4rch1ve")  # lock the door to fractured archive

        # Fractured Archive
        self.rooms["d0"].set_exit("west", self.rooms["c2"])
        self.rooms["d0"].set_exit("north", self.rooms["d1"])

        # Obsolete Hub
        self.rooms["d1"].set_exit("north", self.rooms["d2"])
        self.rooms["d1"].lock_exit("north", "k3rn3l")  # lock the door to system kernel (end)
        self.rooms["d1"].set_exit("south", self.rooms["d0"])

        # System Kernel is endgame (no exits)

    def place_items(self):
        """
            Place Item objects into chosen rooms.
        :return: None
        """
        # a tier items
        # boot sector
        fragmented_blade = Weapon(
            "fragmented_blade",
            "A weak blade formed from unstable data shards.",
            damage=3,
            weight=20
        )
        health_module = Consumable(
            "health_module",
            "A compact utility that repairs corrupted user data. Activating it restores a portion of your health.",
            weight=7,
            heal=2
        )
        self.rooms["a0"].add_item(health_module)
        self.rooms["a0"].add_item(fragmented_blade)

        # b items
        # dead pixels
        first_corruption = Misc(
            "first_corruption.log",
            "A corrupted monster's log containing forgotten memories.",
            weight=4,
            misc_id="lore2"
        )
        self.rooms["b3"].add_item(first_corruption)

        # data well
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

        # corrupted arsenal
        backpack_upgrade = Misc(
            "storage_expansion",
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
        # phantom node
        signal_tuner = Consumable(
            "signal_tuner",
            "A device that stabilises your attacks temporarily.",
            weight="16",
            heal=0
        )
        self.rooms["c0"].add_item(signal_tuner)

        # d tier items
        # fractured archive
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
        # lost cache
        puzzle_a1 = Puzzle(
            name="reconstruction",
            prompt="Reconstruct the missing byte: 101_01 → what number completes the sequence?",
            solution="0",
            reward=Misc(
                "phantom_key",
                "A strange shard that faints in and out of existence.",
                weight=4,
                misc_id="unlock_c0"
            )
        )
        self.rooms["a1"].puzzle = puzzle_a1

        # data well
        puzzle_b1 = Puzzle(
            name="binary_code",
            prompt="Decode the binary sequence: 0100 0001 = ? (ASCII)",
            solution="A",
            reward=Weapon(
                name="debugging_lance",
                description="A long digital spear forged from stabilised error logs. It hums with corrective energy.",
                weight=32,
                damage=5
            )  # reward is a weapon that defeats data_wraith
        )
        self.rooms["b1"].puzzle = puzzle_b1

        # corrupted arsenal
        puzzle_b2 = Puzzle(
            name="kernel_repair",
            prompt="Repair the corrupted kernel header: K_RN_L → fill the missing letters.",
            solution="KERNEL",    # accepting "KERNEL" in game logic is easy too
            reward=Consumable(
                name="health_container",
                description="A large utility that immensely repairs corrupted user data. Activating it restores a large portion of your health.",
                heal=5,
                weight=8
            )  # unlock a large health_container
        )
        self.rooms["b2"].puzzle = puzzle_b2

        # phantom node
        puzzle_c0 = Puzzle(
            name="faded_data",
            prompt="A whisper: 'What remains when memory fades?'",
            solution="echo",
            reward=None  # optional: can spawn lore item if you want
        )
        self.rooms["c0"].puzzle = puzzle_c0

        # obsolete hub
        puzzle_d1 = Puzzle(
            name="kernel_bypass",
            prompt="Enter the decryption key: XOR(7, 12) = ?",
            solution="11",
            reward="kernel_key"  # unlocks passage to System Kernel
        )
        self.rooms["d1"].puzzle = puzzle_d1

    def place_monsters(self):
        """
            Assign Monster objects to chosen rooms.
        :return: None
        """
        # glitch pit
        glitch_beast = Monster(
            name="glitch_beast",
            description="A twitching creature made of broken meshes and flickering polygons.",
            hp=6,
            max_hp=6,
            attack_power=2,
            reward=Misc(
                "data_key",
                "A glowing access shard designed to unlock the Data Well gateway.",
                weight=8,
                misc_id="4rch1ve"
            ),
            blocks_exit="east"
        )
        self.rooms["b0"].add_monster(glitch_beast)

        # data well
        data_wraith = Monster(
            name="data_wraith",
            description="A humanoid shape made of streaming binary. Its form shifts unpredictably.",
            hp=10,
            max_hp=10,
            attack_power=3,
            reward=Misc(
                "integrity_recompiler",
                description="An ancient subsystem tool once used by the system administrators. It rewrites part of your core, patching deep corruption and increases your maximum health.",
                weight=16,
                misc_id="health_upgrade"
            ),
            blocks_exit="south"
        )
        self.rooms["b1"].add_monster(data_wraith)

        # corrupted arsenal
        corrupted_drone = Monster(
            name="corrupted_drone",
            description="A floating defense unit, its casing fractured and emitting sparks.",
            hp=14,
            max_hp=14,
            attack_power=4,
            reward=None
        )
        self.rooms["b2"].add_monster(corrupted_drone)

        # phantom node
        echo_shade = Monster(
            name="echo_shade",
            description="A faint silhouette, like a shadow of code that never fully loads.",
            hp=12,
            max_hp=12,
            attack_power=4,
            reward=None
        )
        self.rooms["c0"].add_monster(echo_shade)

        # gatekeeper node
        gatekeeper = Monster(
            name="gatekeeper",
            description=(
                "A massive corrupted guardian flickering between frames. It guards the kernel path."
            ),
            hp=25,
            max_hp=25,
            attack_power=6,
            reward=Misc("kernel_key", "A critical system key dropped by the Gatekeeper.", weight="16", misc_id="k3rn3l")
        )
        self.rooms["c2"].add_monster(gatekeeper)

        # fractured archive
        memory_phantom = Monster(
            name="memory_phantom",
            description="A ghost formed from corrupted logs and broken memories.",
            hp=15,
            max_hp=15,
            attack_power=5,
            reward=None
        )
        self.rooms["d0"].add_monster(memory_phantom)

