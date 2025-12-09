from room import Room

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
            +----------------------- BOOT SECTOR ------------------------------------+
                System booting...

                    [ Initialising user shell ]
                    [ Loading visual layer    ]
                    [ Syncing input streams   ]

                A plain-looking room forms around you, 
                like the world is still loading.
                Bits of code drip from the ceiling. 
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

    def link_rooms(self):
        """
            Creates directional exits between rooms.
        :return: None
        """
        # set exits
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

    def place_puzzles(self):
        """
            Assign Puzzle objects to chosen rooms.
        :return: None
        """

    def place_monsters(self):
        """
            Assign Monster objects to chosen rooms.
        :return: None
        """

