package maker;

import functional.classes.Location;
import functional.classes.Route;
import functional.classes.TransportationType;
import functional.classes.TravelData;
import visual.Console;
import visual.MenuInitializer;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;

public class CSVMaker {

    public static Console console = MenuInitializer.console;
    public static PrintStream stream = new PrintStream(console);

    public static String routesToCSV (ArrayList<Route> list) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < list.size(); i++) {
            Route route = list.get(i);
            builder.append("(").append(route.getId()).append(",")
                    .append(route.getFrom()).append(",")
                    .append(route.getEuro_price()).append(",")
                    .append(route.getTrip_duration()).append(",")
                    .append(route.getTravel_data()).append(")");
            if (i == list.size() - 1) {
                builder.append(";");
            } else {
                builder.append(",");
            }
        }
        return builder.toString();
    }

    public static String locationsToCSV (ArrayList<Location> list) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < list.size(); i++) {
            Location location = list.get(i);
            builder.append("(").append(location.getId()).append(",")
                    .append(location.getName()).append(",")
                    .append(location.getLatitude()).append(",")
                    .append(location.getLongitude()).append(")");
            if (i == list.size() - 1) {
                builder.append(";");
            } else {
                builder.append(",");
            }
        }
        return builder.toString();
    }

    public static String travelDataToCSV (ArrayList<TravelData> list) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < list.size(); i++) {
            TravelData data = list.get(i);
            builder.append("(").append(data.getId()).append(",")
                    .append(data.getFrom()).append(",")
                    .append(data.getTo()).append(",")
                    .append(data.getTransportation_type()).append(",")
                    .append(data.getEuro_price()).append(",")
                    .append(data.getTime_in_minutes()).append(")");
            if (i == list.size() - 1) {
                builder.append(";");
            } else {
                builder.append(",");
            }
        }
        return builder.toString();
    }

    public static String transportationTypesToCSV (ArrayList<TransportationType> list) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < list.size(); i++) {
            TransportationType type = list.get(i);
            builder.append("(").append(type.getId()).append(",")
                    .append(type.getName()).append(")");
            if (i == list.size() - 1) {
                builder.append(";");
            } else {
                builder.append(",");
            }
        }
        return builder.toString();
    }

    public static void routesToFile(String input, String folder, String routeType) {
        try (FileWriter file = new FileWriter(folder + "/" + routeType + ".csv")) {
            file.write(input);
            file.flush();
            stringMaker(routeType + ".csv created");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void stringToFile(String input, String folder, String filename) {
        try (FileWriter file = new FileWriter(folder + "/" + filename + ".csv")) {
            file.write(input);
            file.flush();
            stringMaker(filename + ".csv created");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void validationToFile(String input, String folder, String routeType) {
        try (FileWriter file = new FileWriter(folder + "/" + routeType + ".csv")) {
            file.write(input);
            file.flush();
            stringMaker("Validation of " + routeType + ".csv created");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void stringMaker (String input) {
        System.out.println(input);
        stream.println(input);
    }
}
