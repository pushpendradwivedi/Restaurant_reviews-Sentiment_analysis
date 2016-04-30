import java.io.*;
import java.util.*;
 
public class append{

	public static void main (String args[])
	{	
		try{
			FileInputStream fstream = new FileInputStream("pos.yml");
			//FileInputStream fstream = new FileInputStream("neg.yml");
			BufferedReader br = new BufferedReader(new InputStreamReader(fstream));
			BufferedWriter bw = new BufferedWriter(new FileWriter(new File("positive.yml"), true));
			//BufferedWriter bw = new BufferedWriter(new FileWriter(new File("negative.yml"), true));

			String strLine;

			while ((strLine = br.readLine()) != null)   {
				bw.write(strLine + ": [positive]");
				//bw.write(strLine + ": [negative]");
				bw.newLine();

			}
			bw.close();
			fstream.close();
		}
		catch(Exception e){}

    }
}