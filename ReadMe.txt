To Scan Forms in the Second Floor Computer Lab:

1. Login to OpScan Computer: User/Pass -> opscan/opscan
1. In RemarkOEM: Open Template, NCS/Math/CordyCSV <- (something like that).
2. Scan Forms for one section. Ignore blanks/multiples/etc.
3. Save as ASCII (commas), rename saved file in this format: BCordy-NYAs123-W2016.asc.
4. Move these csvs to a computer with python 2.7.

To Generate Reports:

1. Create new subdirectories, one for each teacher, of a directory containing evalutor.py.
2. Copy .ascs into the appropriate teacher directory.
3. Use python 2.7 to run evaluator.py.
4. Compile the texs it produces.
