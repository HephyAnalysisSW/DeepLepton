for FILE in `ls /eos/vbc/user/maximilian.moser/DeepLepton/v2/step1/2016/ele/*/*/*/*.root`; do python -c "from DeepLepton.Tools.helpers import checkRootFile; print 'Problem in $FILE' if not checkRootFile('root://eos.grid.vbc.ac.at/$FILE', checkForObjects=['tree']) else 'OK: $FILE'"; done

#for FILE in `ls /scratch-cbe/users/maximilian.moser/DeepLepton/traindata/DYvsQCD_2016/*.root`; do python -c "from DeepLepton.Tools.helpers import checkRootFile; print 'Problem in $FILE' if not checkRootFile('$FILE', checkForObjects=['tree']) else 'OK: $FILE'"; done

#/scratch-cbe/users/maximilian.moser/DeepLepton/traindata/DYvsQCD_2016/i

#for FILE in `ls /eos/vbc/user/maximilian.moser/DeepLepton/v2/step1/2016/ele/*/*/*/*.root`; do python -c "from DeepLepton.Tools.helpers import checkRootFile; print 'Problem in $FILE' if not checkRootFile('root://eos.grid.vbc.ac.at/$FILE', checkForObjects=['tree']) else 'OK: $FILE'"; done
