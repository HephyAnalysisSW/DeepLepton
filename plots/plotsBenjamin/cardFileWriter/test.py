from Analysis.Tools.cardFileWriter import cardFileWriter

c = cardFileWriter.cardFileWriter()

cardFileNameTxt = "./card_file.txt"

processes = [ "tt" ]


c.addUncertainty( "lumi", "lnN" )

c.addBin("SR", processes )
c.specifyExpectation( "SR", "signal", 100. )
c.specifyExpectation( "SR", "tt", 5000. )
c.specifyObservation( "SR", 5000)

c.addBin("SR2", processes )
c.specifyExpectation( "SR2", "signal", 50. )
c.specifyExpectation( "SR2", "tt", 25. )
c.specifyObservation( "SR2", 25)

for p in processes+["signal"]:
    c.specifyUncertainty( "lumi", "SR", p, 1.036 )
    c.specifyUncertainty( "lumi", "SR2", p, 1.036 )

c.writeToFile( cardFileNameTxt )

c.calcLimit()


