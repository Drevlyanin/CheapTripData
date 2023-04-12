package pystarter.pypart.src;

import visual.Console;
import visual.MenuInitializer;

import java.io.*;

public class PyStarter {

    public static Console console = MenuInitializer.console;
    public static PrintStream stream = new PrintStream(console);

    public static void starter(String path) throws IOException, InterruptedException {
        ProcessBuilder pb = new ProcessBuilder("python", "pipeline.py");
        pb.directory(new File(path + "/src/main/java/pystarter/pypart/src"));
        try {
            Process p = pb.start();
            stringMaker("Pipeline process started");
            pythonConsoleMaker(p);
        } catch (IOException e) {
            stringMaker("Error during the pipeline");
        }
        stringMaker("Pipeline process finished");
    }

    public static void pythonConsoleMaker(Process process) throws IOException, InterruptedException{
        InputStream stdout = process.getInputStream();
        InputStream stderr = process.getErrorStream();
        InputStreamReader isr = new InputStreamReader(stdout);
        InputStreamReader isrerr = new InputStreamReader(stderr);
        BufferedReader br = new BufferedReader(isr);
        BufferedReader brerr = new BufferedReader(isrerr);

        String line = null;

        while ((line = br.readLine()) != null) {
            System.out.println(line);
        }

        while ((line = brerr.readLine()) != null) {
            System.out.println(line);
        }
        process.waitFor();
    }

    public static void stringMaker (String input) {
        System.out.println(input);
        stream.println(input);
    }
}
