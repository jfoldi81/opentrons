

from opentrons import protocol_api
from opentrons import simulate
protocol = simulate.get_protocol_api('2.8')

metadata = {'apiLevel': '2.8',
               'protocolName': 'Serial Dilution Tutorial group 4',
    'description': '''This protocol is to implement the iGem protocol. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.''',
    'author': 'Group Four'}

def run(protocol:protocol_api.ProtocolContext):

    # def run(protocol:protocol_api.ProtocolContext):
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 4)
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 7)
    tiprack_3 = protocol.load_labware('opentrons_96_tiprack_300ul', 10)

    p300 = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tiprack_1,tiprack_2,tiprack_3])
    reservoir = protocol.load_labware('4ti0131_12_reservoir_21000ul', 1)
    plate = protocol.load_labware('costar3370flatbottomtransparent_96_wellplate_200ul', 2)
    plate_antigen = protocol.load_labware('costar3370flatbottomtransparent_96_wellplate_200ul', 3)
    trash = protocol.load_labware('4ti0131_12_reservoir_21000ul', 11)

    #what do we put into the reservoir
    #A1 - coating buffer - for serial dilutions
    #A2 - blocking buffer

    #setting up the dilution plate
    #adding the antigen solution to col 1
    p300.transfer(200, plate_antigen.rows()[0][:1], plate.rows()[0][:1], mix_after=(3, 50))
    #adding the coating solution to the other wells for the serial dilutions
    p300.transfer(100, reservoir["A1"], plate.rows()[0][1:6])
    #making dilutions from col 1 to col 5
    p300.transfer(100, plate.rows()[0][:5], plate.rows()[0][1:6], mix_after=(3, 50))
    #empty the extra 100 uL from col 6
    p300.transfer(100, plate.rows()[0][5], trash["A1"])#, mix_after=(3, 50))

    #wait for 2 hours at room temp - at this time, flip the tiprack so that new tips are on the left - now shoudl have 8 cols left
    p300.transfer(100, plate.rows()[0][:5], trash["A1"])#, mix_after=(3, 50))




    #add 200 uL blocking buffer to every well
    p300.transfer(200, reservoir["A3"], plate.rows()[0][:6])
    #wait 1-2 hours at room temp
    #dump out blockign buffer
    p300.transfer(200,plate.rows()[0][:6], trash["A1"])

    #wash with 100 uL of PBS 3 times
    for wash in range(3):
        p300.transfer(100,reservoir["A2"] , plate.rows()[0][:6], mix_after=(1, 50))
        p300.transfer(100,plate.rows()[0][:6], trash["A1"])

    #chekc how much volume to use per wash

    #add 100 uL primary antibody to every well
    p300.transfer(100, reservoir["A4"], plate.rows()[0][:6])
    #wait 1-2 hours
    #dump out solution
    p300.transfer(100,plate.rows()[0][:6], trash["A2"])
    #wash with 100 uL of PBS 3 times
    for wash in range(3):
        p300.transfer(100,reservoir["A2"] , plate.rows()[0][:6], mix_after=(1, 50))
        p300.transfer(100,plate.rows()[0][:6], trash["A2"])


    #add 100 uL secondary antibody to every well
    p300.transfer(100, reservoir["A5"], plate.rows()[0][:6])
    #wait 1-2 hours
    #dump out solution
    p300.transfer(100,plate.rows()[0][:6], trash["A2"])

    #add PBS and agitate for 5 minutes
    p300.transfer(100,reservoir["A2"] , plate.rows()[0][:6], mix_after=(1, 50))
    ###AGITATE FOR 5 MINUTES#####
    p300.transfer(100,plate.rows()[0][:6], trash["A2"])
    #wash with 100 uL of PBS 3 times
    for wash in range(3):
        p300.transfer(100,reservoir["A2"] , plate.rows()[0][:6], mix_after=(1, 50))
        p300.transfer(100,plate.rows()[0][:6], trash["A2"])

    #mix the PNPP by hand then add to reservoir column A6
    p300.transfer(100, reservoir["A6"], plate.rows()[0][:6], mix_after=(3, 50))
    #incubate fro 15- 30 minutes
    #add 50 uL of NaOH
    p300.transfer(50, reservoir["A7"], plate.rows()[0][:6], mix_after=(3, 50))











    return

