% Example script for direct communication with sessantaquattro
%
% Include the "ACCELEROMETER" mode
%
% OT Bioelettronica
% v 2.1

close all
clear all

FSAMP = 0;      % if MODE != 3: 0 = 500 Hz,  1 = 1000 Hz, 2 = 2000 Hz
                % if MODE == 3: 0 = 2000 Hz, 1 = 4000 Hz, 2 = 8000 Hz
NCH  = 0;       % 0 = 8 channels, 1 = 16 channels, 2 = 32 channels, 3 = 64 channels
MODE = 3;       % 0 = Monopolar, 1 = Bipolar, 2 = Differential, 3 = Accelerometers, 6 = Impedance check, 7 = Test Mode
HRES = 1;       % 0 = 16 bits, 1 = 24 bits
HPF  = 0;       % 0 = DC coupled, 1 = High pass filter active
EXTEN = 0;      % 0 = standard input range, 1 = double range, 2 = range x 4, 3 = range x 8
TRIG = 0;       % 0 = Data transfer and REC on SD controlled remotely, 3 = REC on SD controlled from the pushbutton
GO   = 1;       % 0 = just send the settings, 1 = send settings and start the data transfer

ConvFact = 0.000286;

Command = 0;

Command = Command + GO;
Command = Command + TRIG * 4;
Command = Command + EXTEN * 16;
Command = Command + HPF * 64;
Command = Command + HRES * 128;
Command = Command + MODE * 256;
Command = Command + NCH * 2048;
Command = Command + FSAMP * 8192;

dec2bin(Command) %dec2bin(23) -> 10111

switch NCH
    case 0
        if(MODE == 1)
            NumChan = 8;
        else
            NumChan = 12;
        end
    case 1
        if(MODE == 1)
            NumChan = 12;
        else
            NumChan = 20;
        end
    case 2
        if(MODE == 1)
            NumChan = 20;
        else
            NumChan = 36;
        end
    case 3
        if(MODE == 1)
            NumChan = 36;
        else
            NumChan = 68;
        end
end

switch FSAMP
    case 0
        if(MODE == 3)
            sampFreq = 2000;
        else
            sampFreq = 500;
        end
    case 1
        if(MODE == 3)
            sampFreq = 4000;
        else
            sampFreq = 1000;
        end
    case 2
        if(MODE == 3)
            sampFreq = 8000;
        else
            sampFreq = 2000;
        end
    case 3
        if(MODE == 3)
            sampFreq = 16000;
        else
            sampFreq = 4000;
        end
    otherwise
        disp('wrong value for FSAMP')
end


t = tcpip('0.0.0.0', 45454, 'NetworkRole', 'server');
t.InputBufferSize = 500000;

fopen(t)

blockData = 2*NumChan*sampFreq;

disp('Connected to the Socket')

fwrite(t, Command, 'int16');

if(HRES == 1)

    ChInd = (1:3:NumChan*3);

    % Main plot loop
    for i = 1 : 10

        i

        while(t.BytesAvailable < blockData)
        end

        Temp = fread(t, [NumChan * 3, sampFreq], 'uint8');
        data{i} = Temp(ChInd,:)*65536 + Temp(ChInd+1,:)*256 + Temp(ChInd+2,:);
        ind = find(data{i} >= 8388608);
        data{i}(ind) = data{i}(ind) - (16777216);

        %subplot(4,1,1:2)
        hold off
        for j = 1 : 4
            plot(data{i}(j,:)*ConvFact + 0.1*(j-1));
            hold on
        end

        drawnow;
    end
else
    % Main plot loop
    for i = 1 : 10

        i

        while(t.BytesAvailable < blockData)
        end
        
        data{i} = fread(t, [NumChan, sampFreq], 'int16');

        subplot(2,1,1)
        hold off
        for j = 1 : NumChan-4
            plot(data{i}(j,:)*ConvFact + 0.5*(j-1));
            hold on
        end

        subplot(2,1,2)
        plot(data{i}(NumChan-1,:));
        drawnow;
    end
end


fwrite(t, Command-1, 'int16');

fclose(t)
