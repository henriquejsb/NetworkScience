python3 pageRank.py filename beta CSV


	Where filename is the name of the file where the graph is, in edge list format (similar to last homework); beta is the value for beta; 

File format:
N
n1 n2
...

N - number of the nodes of the graph
n1 n2 - edge between n1 and n2


	CSV should be “Y” if the number of iterations is too big, since the program will output the ranks per iteration in CSV fashion. To store in CSV, run as 
	
	pageRank.py filename beta CSV > outfile
	

There is also a file called plotter.py. To run it  use:
python3 plotter.py filename minbeta maxbeta step
This will run pageRank for the graph in filename with beta values in [minbeta,maxbeta] with increments of “step”. 

It will plot the graphics required in exercise 5 in “filename_plot.png”.
