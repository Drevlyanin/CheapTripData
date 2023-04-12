package parser;

import functional.classes.Location;
import functional.classes.TravelData;
import maker.classes.OldLocationsMaker;
import visual.Console;
import visual.MenuInitializer;

import java.io.*;
import java.util.ArrayList;

public class ParserForCounter {

    public static Console console = MenuInitializer.console;
    public static PrintStream stream = new PrintStream(console);

    public static String[] CSVoString(String fileName) throws IOException {
        File file = new File(fileName);
        FileReader fr = new FileReader(file);
        BufferedReader reader = new BufferedReader(fr);
        String line = "";
        String add = "";
        while (add != null) {
            String str = "";
            add = reader.readLine();
            if (add == null) {
                str = "";
            } else {
                str = "(" + add + "),";
            }
            line = line + str;
        }

        String[] lines = line.split("\\),\\(");
        for (int i = 0; i < lines.length; i++) {
            lines[i] = lines[i].replaceAll("[(')]", "");
            lines[i] = lines[i].replaceAll("null", "");
        }
        return lines;
    }

    public static ArrayList<Location> insertLocations(String[] input) {
        ArrayList<Location> oldLocation = OldLocationsMaker.getOldLocations();
        int k = input.length;
        ArrayList<Location> locations = new ArrayList<>();
        for (int i = 0; i < k; i++) {
            if (!input[i].startsWith("id_city")) {
                String[] arr = input[i].split(",");
                int id = Integer.parseInt(arr[0]);
                String name = arr[1];
                double latitude = Float.parseFloat(arr[2]);
                double longitude = Float.parseFloat(arr[3]);
                String country_name = null;
                for (int j = 0; j < oldLocation.size(); j++) {
                    Location location = oldLocation.get(j);
                    if (id == location.getId() && name.equals(location.getName())) {
                        country_name = location.getCountry_name();
                    } else if (id == location.getId()) {
                        country_name = location.getCountry_name();
                    }
                }
                Location result = new Location(id,name,latitude,longitude,country_name);
                locations.add(result);
            }
        }
        stringMaker("Locations successfully parsed");
        return locations;
    }

    public static ArrayList<TravelData> insertTravelData(String[] input) {
        int k = input.length;
        ArrayList<TravelData> datas = new ArrayList<>();
        for (int i = 0; i < k; i++) {
            if (!input[i].startsWith("path_id")) {
                String[] arr = input[i].split(",");
                TravelData data = new TravelData(
                        Integer.parseInt(arr[0]),
                        Integer.parseInt(arr[1]),
                        Integer.parseInt(arr[2]),
                        Integer.parseInt(arr[3]),
                        Float.parseFloat(arr[4]),
                        Integer.parseInt(arr[5])
                );
                datas.add(data);
            }
        }
        stringMaker("Direct routes successfully parsed");
        return datas;
    }

    public static String locationsToString(ArrayList<Location> list) {
        String result = "";
        for (int i = 0; i < list.size(); i++) {
            Location location = list.get(i);
            String add = "Id = " + location.getId() + "," +
                    "Name = " + location.getName() + "," +
                    "Latitude = " + location.getLatitude() + "," +
                    "Longitude = " + location.getLongitude() + "\n";
            result = result + add;
        }
        return result;
    }

    public static String travelDataToString(ArrayList<TravelData> list) {
        String result = "";
        for (int i = 0; i < list.size(); i++) {
            TravelData directRoute = list.get(i);
            String add = "Id = " + directRoute.getId() + "," +
                    "`from` = " + directRoute.getFrom() + "," +
                    "`to` = " + directRoute.getTo() + "," +
                    "transportation_type = " + directRoute.getTransportation_type() + "," +
                    "euro_price = " + directRoute.getEuro_price() + "," +
                    "time_in_minutes = " + directRoute.getTime_in_minutes() + "\n";
            result = result + add;
        }
        return result;
    }
    public static void stringMaker (String input) {
        System.out.println(input);
        stream.println(input);
    }
}
