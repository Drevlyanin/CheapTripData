package visual.classes;

import visual.Console;
import visual.MenuInitializer;

import java.io.PrintStream;

public class LocationsFolderChecker {

    public static Console console = MenuInitializer.console;
    public static PrintStream stream = new PrintStream(console);

    public static boolean locationsChecker (String input) {
        if (input.equals("")) {
            stringMaker("No file with locations");
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
