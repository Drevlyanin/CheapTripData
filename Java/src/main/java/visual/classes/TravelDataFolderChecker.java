package visual.classes;

import visual.Console;
import visual.MenuInitializer;

import java.io.PrintStream;

public class TravelDataFolderChecker {

    public static Console console = MenuInitializer.console;
    public static PrintStream stream = new PrintStream(console);

    public static boolean travelDataChecker (String input) {
        if (input.equals("")) {
            stringMaker("No file with travel_data");
            return false;
        } else {
            return true;
        }
    }

    public static void stringMaker (String input) {
        System.out.println(input);
        stream.println(input);
    }
}
