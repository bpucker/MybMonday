### Boas Pucker ###
### b.pucker@tu-braunschweig.de ###
### v0.1 ###

__usage__ = """
					python3 papers2table.py
					--in <INPUT_FILE>
					--out <OUTPUT_FILE>
					
					optional:
					--sort <SORT_MODUS>(fam|author|year|spec|none)[none]
					bug reports and feature requests: b.pucker@tu-braunschweig.de
					"""

import os, sys
from operator import itemgetter

# --- end of imports --- #

def load_data( input_file ):
	"""! @brief load all data sets and header """
	
	data = []
	with open( input_file, "r" ) as f:
		headers = f.readline().strip().split('\t')
		line = f.readline()
		while line:
			parts = line.strip().split('\t')
			entry = {}
			try:
				for idx, header in enumerate( headers ):
					entry.update( { header: parts[ idx ] } )
			except IndexError:
				print( line )
			data.append( entry )
			line = f.readline()
	return data, headers


def main( arguments ):
	"""! @brief run everything """
	
	input_file = arguments[ arguments.index('--in')+1 ]
	output_file = arguments[ arguments.index('--out')+1 ]
	
	if "--sort" in arguments:
		sort_modus = arguments[ arguments.index('--sort')+1 ]
		if sort_modus not in [ "fam", "author", "year", "spec", "none" ]:
			sort_modus = "none"
	else:
		sort_modus = "none"
	
	
	data, headers = load_data( input_file )
	
	if sort_modus == "fam":
		data = sorted( data, key=itemgetter('Family', 'Species') )
	elif sort_modus == "author":
		data = sorted( data, key=itemgetter('Author', 'Year') )
	elif sort_modus == "year":
		data = sorted( data, key=itemgetter('Year', 'Author') )
	elif sort_modus == "spec":
		data = sorted( data, key=itemgetter('Species') )
	
	
	table_fields = [ "Family", "Species", "TrivialName", "MYB_Name", "MYB_Function", "Evidence" ]
	with open( output_file, "w" ) as out:
		out.write( "| " + " | ".join( table_fields + [ "Reference", "Title" ] ) + " |\n" )
		out.write( "| " + "----- | -----"*(len( table_fields + [ "Reference", "Title" ] )-1) + " |\n" )
		for entry in data:
			new_line = []
			for each in table_fields:
				if each == "Species":
					new_line.append( "<i>" + entry[ each ] + "</i>" )
				else:
					new_line.append( entry[ each ] )
			new_line.append( "[" + entry['Author'] + " <i>et al.</i>, " + entry['Year'] + "](" + entry['URL'] + ")" )
			new_line.append( entry['Title'] )
			out.write( "| " + " | ".join( new_line ) + " |\n" )


if '--in' in sys.argv and '--out' in sys.argv:
	main( sys.argv )
else:
	sys.exit( __usage__ )
