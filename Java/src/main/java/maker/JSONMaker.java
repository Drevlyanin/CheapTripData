package maker;

import com.google.gson.JsonObject;
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
import java.util.List;

public class JSONMaker {

    public static Console console = MenuInitializer.console;
    public static PrintStream stream = new PrintStream(console);

    public static ArrayList<JsonObject> locationsJson(List<Location> locations) {
        ArrayList<JsonObject> list = new ArrayList<>();
        for (int i = 0; i < locations.size(); i++) {
            Location location = locations.get(i);
            JsonObject object = new JsonObject();
            object.addProperty("id", location.getId());
            object.addProperty("name", location.getName());
            object.addProperty("latitude", location.getLatitude());
            object.addProperty("longitude", location.getLongitude());
            list.add(object);
        }
        return list;
    }

    public static ArrayList<JsonObject> travelDataJson(List<TravelData> data) {
        ArrayList<JsonObject> list = new ArrayList<>();
        for (int i = 0; i < data.size(); i++) {
            TravelData travelData = data.get(i);
            JsonObject object = new JsonObject();
            object.addProperty("id", travelData.getId());
            object.addProperty("from", travelData.getFrom());
            object.addProperty("to", travelData.getTo());
            object.addProperty("transportation_type", travelData.getTransportation_type());
            object.addProperty("euro_price", travelData.getEuro_price());
            object.addProperty("time_in_minutes", travelData.getTime_in_minutes());
            list.add(object);
        }
        return list;
    }

    public static ArrayList<JsonObject> transportationTypeJson(List<TransportationType> types) {
        ArrayList<JsonObject> list = new ArrayList<>();
        for (int i = 0; i < types.size(); i++) {
            TransportationType type = types.get(i);
            JsonObject object = new JsonObject();
            object.addProperty("id", type.getId());
            object.addProperty("name", type.getName());
            list.add(object);
        }
        return list;
    }

    public static ArrayList<JsonObject> routesJson(List<Route> routes) {
        ArrayList<JsonObject> list = new ArrayList<>();
        for (int i = 0; i < routes.size(); i++) {
            Route route = routes.get(i);
            JsonObject object = new JsonObject();
            object.addProperty("id", route.getId());
            object.addProperty("from", route.getFrom());
            object.addProperty("to", route.getTo());
            object.addProperty("euro_price", route.getEuro_price());
            object.addProperty("trip_duration", route.getTrip_duration());
            object.addProperty("travel_data", route.getTravel_data());
            list.add(object);
        }
        return list;
    }

    public static void jsonToFile(ArrayList<JsonObject> list, String folder, String filename) {
        int k = list.size();
        JsonObject general = new JsonObject();
        for (int i = 0; i < k; i++) {
            general.add(String.valueOf(i + 1), list.get(i));
        }
        try (FileWriter file = new FileWriter(folder + "/" + filename + ".json")) {
            System.out.println(general.toString());
            file.write(general.toString());
            file.flush();
            stringMaker(filename + ".json created");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void stringMaker (String input) {
        System.out.println(input);
        stream.println(input);
    }
}
