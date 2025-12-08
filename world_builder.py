from room import Room

class WorldBuilder:
    def build(self):
        """
            Creates all rooms, connects them with exits,
            places items/puzzles/monsters, and returns the starting room.
        :return: The starting room.
        """



        room_a0 = Room(
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

        room_a1 = Room(
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

        room_b0 = Room(
            "Glitch Pit",
            """
            +-------------------------- GLITCH PIT ----------------------------------+
                The ground seems unreliable here.  
                Tiles appear late, and some just blink in and out of existence.

                    !! Terrain error: mesh failed to load !!
                    A twitching, half-rendered monster notices you.

                This area feels dangerous.

                Exits: NORTH -> Boot Sector, EAST -> Data Well
            +------------------------------------------------------------------------+
            """
        )

        room_b1 = Room(
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

        room_b2 = Room(
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
                
                Exits: NORTH -> Data Well
            +------------------------------------------------------------------------+
            """
        )

        room_c0 = Room(
            "Phantom Node",
            """
            +--------------------------- PHANTOM NODE -------------------------------+
                This room shouldn't exist...  
                Its walls are only half-there, fading in and out like a memory.
                
                   You feel watched.
                   A strange object hovers silently.
                
                This place only appears if you're carrying something special.
                
                Exits: unknown
            +------------------------------------------------------------------------+
            """
        )

        room_c2 = Room(
            "Gatekeeper Node",
            """
            +----------------------- GATEKEEPER NODE --------------------------------+
                A massive corrupted guardian blocks the path ahead.
                It flickers between frames, unfinished and unstable.
                
                   ACCESS DENIED: kernel key required
                   The creature roars and the whole room shudders.
                
                This fight is unavoidable.
                
                Exits: SOUTH -> Fractured Archive (locked until victory)
            +------------------------------------------------------------------------+
            """
        )

        room_d0 = Room(
            "Fractured Archive",
            """
            +----------------------- FRACTURED ARCHIVE ------------------------------+
                Broken bits of past events float around like ghosts.
                Some logs replay wrong. Others don't load at all.
                
                   [ log_04: missing timestamp ]
                   [ memory chunk corrupted    ]
                
                A console sits in the centre, but it needs a decryption item.
                
                Exits: NORTH -> Gatekeeper Node, EAST -> Obsolete Hub
            +------------------------------------------------------------------------+
            """
        )

        room_d1 = Room(
            "Obsolete Hub",
            """
            +--------------------------- OBSOLETE HUB -------------------------------+
                This room feels outdated. Old system functions lie everywhere,  
                half-functional and flickering.
                
                   < deprecated_module >
                   < legacy API called >
                   < unsupported format >
                
                A giant puzzle dominates the middle of the room.
                
                Exits: west -> Fractured Archive, north -> System Kernel
            +------------------------------------------------------------------------+
            """
        )

        room_d2 = Room(
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

    def link_rooms(self):
        """
            Creates directional exits between rooms.
        :return: None
        """

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

