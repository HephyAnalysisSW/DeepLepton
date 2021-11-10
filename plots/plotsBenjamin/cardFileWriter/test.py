from Analysis.Tools.cardFileWriter import cardFileWriter

c = cardFileWriter.cardFileWriter()

cardFileNameTxt = "./card_file.txt"

processes = [ "signal", "tt" ]

c.addBin("SR", processes )


c.specifyExpectation( "SR", "signal", 100. )
c.specifyExpectation( "SR", "tt", 5000. )
c.addUncertainty( "lumi", "lnN" )
c.specifyObservation( "SR", 5000)

for p in processes:
    c.specifyUncertainty( "lumi", "SR", p, 1.036 )

c.writeToFile( cardFileNameTxt )


