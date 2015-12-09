
'''

Notes from Freedom EVOware Sotware manual V2.3
15.24.2 - Worklist file format
- Text file containing pipetting instructions
- Individual lines: "records"
- - Records start with a single character and are followed by 1 or more parameters, separated by semicolons
- Record types available:
    - Aspirate
        - A;RackLabel;RackID;RackType;Position;TubeID;Volume;LiquidClass;TipType;TipMask;ForcedRackType
    - Dispense
        - D;RackLabel;RackID;RackType;Position;TubeID;Volume;LiquidClass;TipType;TipMask;ForcedRackType
        - [see 15.24.2.1 "parameters for aspirate and dispense records", and "15-41 for details)
    - Wash tips / replace DITIs
        - W;
        - W1;
        - W2;
        - W3;
        - W4;
        - Washes the tip or replaced the DITI which was used by the preceding aspirate record
        - No parameters
    - Decontamination wash
        - WD;
        - Decomntamination wash followed by normal wash
        - No parameters
    - Flush
        - F;
        - Discards tip contents without washing them or dropping DITIs
    - Break
        - B;
        - Forces excution of previously specified aspirate/dispense/wash actions which have not yet been executed
        - Always resets the DITI type to the type selected in the worklist command
        - If a Break record is not specified, commands will be executed in groups to optimize efficiency
    - Set DITI type (disposable tip type)
        - S;DITI_index
        - Can only be used at the very beginning of the worklist or directly after a break record
        - 
    - Comment
        - C;comment
        - Ignored by the EVO
    - **Reagent distribution**
        - R;AspirateParameters;DispenseParameters;Volume;LiquidClass;NoOfDitiReuses;NoOfMultiDisp;Direction[;ExcludeDestWell]
        where
            - AspirateParameters=SrcRackLabel;SrcRackID;SrcRackType;SrcPosStart;SrcPosEnd;
            - DispenseParameters = DestRackLabel;DestRackID;DestRackType;DestPostStart;DestPosEnd

- **Parameters for aspirate and dispense records**
    - RackLabel: User-defined label assigned to the labware
    - RackID: labware barcode
    - RackType: labware type
    - **Position:** well position in the labware (1-indexed, increases from rear to front and left to right
    - TubeID: tube barcode
    - **Volume:** Pipetting volume in microL
    - **LiquidClass:** optional parameter overwrites the liquid class specified in worklist command
    - TipMask: optional, specifies the tip to use
    - ForcedRack-Type: optional, configuration name of labware
    - **MinDetectedVolume:** liquid volume in microL -- if specified, and if liquid level detection is enabled
        in the selected liquid class, is used to determine the minimum liquid height which must be available in the well

'''

def add_reagent_to_worklist(source_rack_label,
                            source_rack_id,
                            source_rack_type,
                            source_position,
                            target_rack_label,
                            target_rack_id,
                            target_rack_type,
                            positions,
                            volumes,
                            liquid_class='',
                            tip_mask='',
                            forced_rack_type='',
                            min_detected_volume=''
                    ):
    worklist = []
    for position,volume in zip(positions,volumes):
        # aspirate from source
        worklist.append('A;{0};{1};{2};{3};{4};{5};{6};{7};{8};'.format(\
            source_rack_label,
            source_rack_id,
            source_rack_type,
            source_position,
            volume,
            liquid_class,
            tip_mask,
            forced_rack_type,
            min_detected_volume))
        
        # dispense into target
        worklist.append('D;{0};{1};{2};{3};{4};{5};{6};{7};{8};'.format(\
            target_rack_label,
            target_rack_id,
            target_rack_type,
            position,
            volume,
            liquid_class,
            tip_mask,
            forced_rack_type,
            min_detected_volume))
        
        # wash
        worklist.append('W;')
    return worklist

if __name__=='__main__':
    reagent_names = ['hepes',
                     'K2HPO4',
                     'MPG',
                     'amm_acetate',
                     'TCEP',
                     'glucose',
                     'amino_acids',
                     'folinic_acid',
                     'amp',
                     'GMP',
                     'UMP',
                     'CMP',
                     'cf_extract',
                     'dna',
                     'water']

    target_rack_label='96wellrxnplate'

    # define a random 96-well format experiment
    import numpy as np
    experiment = np.random.randint(3,10,size=(len(reagent_names),96))
    
    # construct a list of worklists, one for each reagent
    worklist = []
    for i,reagent in enumerate(reagent_names):
        worklist.append(add_reagent_to_worklist(reagent,
                                                '',
                                                '',
                                                '',
                                               target_rack_label,
                                               '',
                                               '',
                                               np.arange(96),
                                               experiment[i]))
    # flatten that list of lists
    worklist = [line for sublist in worklist for line in sublist]

    # write the list to CSV for later use
    worklist_name='example_worklist.csv'
    f = open(worklist_name,'w')
    for line in worklist:
        f.write(line+'\n')
    f.close()


