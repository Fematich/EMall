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
	
	public static String parseblock(String block) throws IOException{
		Segmenter sgm = new Segmenter();
		String    endchar  = Character.toString((char) 30);
		String ret = "";
		Scanner sb = new Scanner(block);
		sb.useDelimiter(endchar);
		try{
			String idline=sb.next();
			if(idline.startsWith("\nid=") | idline.startsWith("id=")){
				ret+=idline+endchar;
			}
			else{
				System.out.println("error in idline "+idline);
				return "";
			}
			String tline=sb.next();
			if(tline.startsWith("\ntime=")){
				ret+=tline+endchar;
			}
			else{
				System.out.println("error in tline "+tline);
				return "";
			}
			String uline=sb.next();
			if(uline.startsWith("\nurl=")){
				ret+=uline+endchar;
			}
			else{
				System.out.println("error in uline "+uline);
				return "";
			}
			String title=sb.next();
			if(title.startsWith("\ntitle=")){
				ret+="\ntitle="+sgm.tokenize(title.substring(7))+endchar;
			}
			else{
				System.out.println("error in title "+title);
				return "";
			}
			String body=sb.next();
			if(body.startsWith("\nbody=")){
				ret+="\nbody="+sgm.tokenize(body.substring(6))+endchar+'\n';	
				return ret;
			}
			else{
				System.out.println("error in body "+body);
				return "";
			}
		}
		catch(Exception e){
			System.out.println("other error");
			return "";
		}
	}

	
	public static void parsefile(String file) throws IOException{
		String    endbchar  = Character.toString((char) 31);
		// reading file
		System.out.println("parsing "+file);
		String filepath="/home/mfeys/work/data/event_mall/old_dat/"+file;
//		InputStreamReader read1 = new InputStreamReader(new FileInputStream(filepath), "GBK");
		InputStreamReader read1 = new InputStreamReader(new FileInputStream(filepath), "GB18030");
		BufferedReader br1 = new BufferedReader(read1);
		Scanner s = new Scanner(br1);
		s.useDelimiter(endbchar);
		//writing file
		String newpath = "/home/mfeys/work/data/event_mall/dat180/"+file;
		File wfile = new File(newpath);
		wfile.createNewFile();
		FileWriter fw = new FileWriter(wfile.getAbsoluteFile());
		BufferedWriter bw = new BufferedWriter(fw);
		//error file
		String errpath = "/home/mfeys/work/data/event_mall/dat180/errdat";
		File erfile = new File(errpath);
		erfile.createNewFile();
		FileWriter erfw = new FileWriter(erfile.getAbsoluteFile(),true);
		BufferedWriter erbw = new BufferedWriter(erfw);	
		int correct=0;
		int incorrect=0;
		while (s.hasNext()){
			String block=s.next();
			String parsedBlock = parseblock(block);				
			if(parsedBlock.equals("")){
				erbw.write(block+endbchar);
				correct++;
			}
			else{
				bw.write(parsedBlock+endbchar);
				incorrect++;
			}
		}
		erfw.close();
		fw.close();
		System.out.println("STATS:"+correct+","+incorrect);
	}
	
	public static void parseEfile(String file) throws IOException{
		String    endbchar  = Character.toString((char) 31);
		// reading file
		System.out.println("parsing "+file);
		String filepath="/home/mfeys/work/data/event_mall/old_dat/"+file;
		InputStreamReader read1 = new InputStreamReader(new FileInputStream(filepath));
		BufferedReader br1 = new BufferedReader(read1);
		Scanner s = new Scanner(br1);
		s.useDelimiter(endbchar);
		//writing file
		String newpath = "/home/mfeys/work/data/event_mall/dat/"+file;
		File wfile = new File(newpath);
		wfile.createNewFile();
		FileWriter fw = new FileWriter(wfile.getAbsoluteFile());
		BufferedWriter bw = new BufferedWriter(fw);
		//error file
		String errpath = "/home/mfeys/work/data/event_mall/dat/errdat";
		File erfile = new File(errpath);
		erfile.createNewFile();
		FileWriter erfw = new FileWriter(erfile.getAbsoluteFile(),true);
		BufferedWriter erbw = new BufferedWriter(erfw);	
		while (s.hasNext()){
			String block=s.next();
			String parsedBlock = parseblock(block);				
			if(parsedBlock.equals("")){
				erbw.write(block+endbchar);
			}
			else{
				bw.write(parsedBlock+endbchar);
			}
		}
		erfw.close();
		fw.close();
	}
	
	public static void main(String[] args) throws IOException {
		System.out.println(System.getProperty("file.encoding"));
		for(int i=0;i<112;i++){
			parsefile("dat"+i);
		}
//		parseEfile("err2dat");
	}
}