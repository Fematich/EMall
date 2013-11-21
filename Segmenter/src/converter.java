import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Scanner;


public class converter {

	/**
	 * @param args
	 * @throws IOException 
	 */
	
	public static void parse(String file) throws IOException{
		String    endchar  = Character.toString((char) 30);
		String    endbchar  = Character.toString((char) 31);
		
		Segmenter sgm = new Segmenter();
		// reading file
		System.out.println(file);
		String filepath="/home/mfeys/work/data/event_mall/old_dat/"+file;
		InputStreamReader read1 = new InputStreamReader(new FileInputStream(filepath), "GBK");
		BufferedReader br1 = new BufferedReader(read1);
		Scanner s = new Scanner(br1);
		s.useDelimiter(endchar);
		//writing file
		String newpath = "/home/mfeys/work/data/event_mall/dat/"+file;
		File wfile = new File(newpath);
		wfile.createNewFile();
		FileWriter fw = new FileWriter(wfile.getAbsoluteFile());
		BufferedWriter bw = new BufferedWriter(fw);
		
		while (s.hasNext()){
			String line=s.next();
			//System.out.print("testbegin"+line+"testend");
			//if(line.substring(1,7).equals("title=")){
			if(line.startsWith("\ntitle=")){
				bw.write("\ntitle="+sgm.tokenize(line.substring(7))+endchar);
				//System.out.println("title="+sgm.tokenize(line.substring(6))+endchar+'\n');
				//System.out.println("title");
				
			}
			//else if(line.substring(1,6).equals("body=")){
			else if(line.startsWith("\nbody=")){
				bw.write("\nbody="+sgm.tokenize(line.substring(6))+endchar);
				//System.out.println("body="+sgm.tokenize(line.substring(5))+endchar);
				//System.out.println("body");
				
			}
			else{
				bw.write(line+endchar);
				//System.out.println(line+endchar);
			}
		}
	}
	
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		//String file=args[0];
//		String file="dat0";
//		System.out.println("main function, calling:"+file);
		for(int i=0;i<112;i++){
			parse("dat"+i);
		}
	}
}

