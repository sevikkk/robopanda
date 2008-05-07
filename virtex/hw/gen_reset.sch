VERSION 6
BEGIN SCHEMATIC
    BEGIN ATTR DeviceFamilyName "virtexe"
        DELETE all:0
        EDITNAME all:0
        EDITTRAIT all:0
    END ATTR
    BEGIN NETLIST
        SIGNAL XLXN_35
        SIGNAL XLXN_67
        SIGNAL XLXN_183
        SIGNAL reset
        SIGNAL locked
        SIGNAL clk
        SIGNAL XLXN_194
        SIGNAL XLXN_195
        PORT Output reset
        PORT Input locked
        PORT Input clk
        BEGIN BLOCKDEF cb4ce
            TIMESTAMP 2000 1 1 10 10 10
            RECTANGLE N 64 -512 320 -64 
            LINE N 0 -32 64 -32 
            LINE N 0 -128 64 -128 
            LINE N 384 -256 320 -256 
            LINE N 384 -320 320 -320 
            LINE N 384 -384 320 -384 
            LINE N 384 -448 320 -448 
            LINE N 80 -128 64 -144 
            LINE N 64 -112 80 -128 
            LINE N 384 -128 320 -128 
            LINE N 192 -32 64 -32 
            LINE N 192 -64 192 -32 
            LINE N 0 -192 64 -192 
            LINE N 384 -192 320 -192 
        END BLOCKDEF
        BEGIN BLOCKDEF fdre_1
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 0 -192 64 -192 
            LINE N 0 -256 64 -256 
            LINE N 384 -256 320 -256 
            LINE N 0 -32 64 -32 
            RECTANGLE N 64 -320 320 -64 
            LINE N 192 -64 192 -32 
            LINE N 192 -32 64 -32 
            LINE N 64 -112 80 -128 
            LINE N 80 -128 64 -144 
            LINE N 0 -128 40 -128 
            CIRCLE N 40 -140 64 -116 
        END BLOCKDEF
        BEGIN BLOCKDEF inv
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 0 -32 64 -32 
            LINE N 224 -32 160 -32 
            LINE N 64 -64 128 -32 
            LINE N 128 -32 64 0 
            LINE N 64 0 64 -64 
            CIRCLE N 128 -48 160 -16 
        END BLOCKDEF
        BEGIN BLOCKDEF vcc
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 64 -32 64 -64 
            LINE N 64 0 64 -32 
            LINE N 96 -64 32 -64 
        END BLOCKDEF
        BEGIN BLOCK XLXI_46 cb4ce
            PIN C clk
            PIN CE XLXN_183
            PIN CLR XLXN_194
            PIN CEO XLXN_67
            PIN Q0
            PIN Q1
            PIN Q2
            PIN Q3
            PIN TC
        END BLOCK
        BEGIN BLOCK XLXI_51 fdre_1
            PIN C clk
            PIN CE XLXN_67
            PIN D XLXN_183
            PIN R XLXN_194
            PIN Q XLXN_35
        END BLOCK
        BEGIN BLOCK XLXI_52 inv
            PIN I XLXN_35
            PIN O reset
        END BLOCK
        BEGIN BLOCK XLXI_48 vcc
            PIN P XLXN_183
        END BLOCK
        BEGIN BLOCK XLXI_53 inv
            PIN I locked
            PIN O XLXN_194
        END BLOCK
    END NETLIST
    BEGIN SHEET 1 3520 2720
        INSTANCE XLXI_46 992 1072 R0
        INSTANCE XLXI_51 1088 1552 R0
        INSTANCE XLXI_52 1520 1328 R0
        BEGIN BRANCH XLXN_35
            WIRE 1472 1296 1520 1296
        END BRANCH
        BEGIN BRANCH XLXN_67
            WIRE 1024 1168 1024 1360
            WIRE 1024 1360 1088 1360
            WIRE 1024 1168 1440 1168
            WIRE 1376 880 1440 880
            WIRE 1440 880 1440 1168
        END BRANCH
        INSTANCE XLXI_48 816 752 R0
        BEGIN BRANCH XLXN_183
            WIRE 880 752 880 880
            WIRE 880 880 960 880
            WIRE 960 880 960 1296
            WIRE 960 1296 1088 1296
            WIRE 960 880 992 880
        END BRANCH
        BEGIN BRANCH reset
            WIRE 1744 1296 1824 1296
        END BRANCH
        IOMARKER 1824 1296 reset R0 28
        BEGIN BRANCH clk
            WIRE 560 944 912 944
            WIRE 912 944 912 1424
            WIRE 912 1424 1088 1424
            WIRE 912 944 992 944
        END BRANCH
        BEGIN BRANCH locked
            WIRE 560 1216 592 1216
        END BRANCH
        IOMARKER 560 1216 locked R180 28
        INSTANCE XLXI_53 592 1248 R0
        IOMARKER 560 944 clk R180 28
        BEGIN BRANCH XLXN_194
            WIRE 816 1216 992 1216
            WIRE 992 1216 992 1248
            WIRE 992 1248 992 1520
            WIRE 992 1520 1088 1520
            WIRE 992 1040 992 1216
        END BRANCH
    END SHEET
END SCHEMATIC
