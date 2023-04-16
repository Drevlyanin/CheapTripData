package maker;

import com.google.gson.JsonObject;
import functional.classes.Location;
import functional.classes.Route;
import functional.classes.TransportationType;
import functional.classes.TravelData;
import parser.ParserForCounter;
import visual.Console;
import visual.MenuInitializer;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class NewJSONMaker {

    public static Console console = MenuInitializer.console;
    public static PrintStream stream = new PrintStream(console);

    public static JsonObject locationsJson(List<Location> locations) {
        JsonObject general = new JsonObject();
        for (int i = 0; i < locations.size(); i++) {
            Location location = locations.get(i);
            JsonObject object = new JsonObject();
            int id = location.getId();
            object.addProperty("name", location.getName());
            object.addProperty("latitude", location.getLatitude());
            object.addProperty("longitude", location.getLongitude());
            object.addProperty("country_name", location.getCountry_name());
            general.add(String.valueOf(id),object);
        }
        return general;
    }

    public static JsonObject travelDataJson(List<TravelData> data) {
        JsonObject general = new JsonObject();
        for (int i = 0; i < data.size(); i++) {
            TravelData travelData = data.get(i);
            JsonObject object = new JsonObject();
            int id = travelData.getId();
            object.addProperty("from", travelData.getFrom());
            object.addProperty("to", travelData.getTo());
            object.addProperty("transport", travelData.getTransportation_type());
            object.addProperty("price", (int)travelData.getEuro_price());
            object.addProperty("duration", travelData.getTime_in_minutes());
            general.add(String.valueOf(id),object);
        }
        return general;
    }

    public static void directRoutesJsonPartly(List<TravelData> data, List<Location> locations,
                                              String path) throws IOException {
        folderForPartlyMaker(path,"direct_routes");
        Collections.sort(data) ;
        for (int i = 0; i < locations.size(); i++) {
            Location location = locations.get(i);
            JsonObject general = new JsonObject();
            List<TravelData> list = new ArrayList<>();
            for (int j = 0; j < data.size(); j++) {
                TravelData direct = data.get(j);
                if (direct.getFrom() == location.getId()) {
                    list.add(direct);
                }
            }
            if (!list.isEmpty()) {
                for (int j = 0; j < list.size(); j++) {
                    TravelData travelData = list.get(j);
                    JsonObject object = new JsonObject();
                    int to = travelData.getTo();
                    object.addProperty("transport", travelData.getTransportation_type());
                    object.addProperty("price", (int) travelData.getEuro_price());
                    object.addProperty("duration", travelData.getTime_in_minutes());
                    general.add(String.valueOf(to), object);
                }
                jsonToFile(general, path + "/partly/direct_routes", String.valueOf(location.getId()));
            }
        }
    }

    public static JsonObject transportationTypeJson(List<TransportationType> types) {
        JsonObject general = new JsonObject();
        for (int i = 0; i < types.size(); i++) {
            TransportationType type = types.get(i);
            JsonObject object = new JsonObject();
            int id = type.getId();
            object.addProperty("name", type.getName());
            general.add(String.valueOf(id),object);
        }
        return general;
    }

    public static JsonObject routesJson(List<Route> routes) {
        JsonObject general = new JsonObject();
        for (int i = 0; i < routes.size(); i++) {
            Route route = routes.get(i);
            JsonObject object = new JsonObject();
            int id = route.getFrom() * 10000 + route.getTo();
            object.addProperty("from", route.getFrom());
            object.addProperty("to", route.getTo());
            object.addProperty("price", (int)route.getEuro_price());
            object.addProperty("duration", route.getTrip_duration());
            object.addProperty("direct_routes", route.getTravel_data());
            general.add(String.valueOf(id),object);
        }
        return general;
    }

    public static void routesJsonPartly (List<Route> routes, List<Location> locations,
                                               String path, String routeType) throws IOException {
        folderForPartlyMaker(path,routeType);
        for (int i = 0; i < locations.size(); i++) {
            Location location = locations.get(i);
            JsonObject general = new JsonObject();
            List<Route> list = new ArrayList<>();
            for (int j = 0; j < routes.size(); j++) {
                Route route = routes.get(j);
                if (route.getFrom() == location.getId()) {
                    list.add(route);
                }
            }
            if (!list.isEmpty()) {
                for (int j = 0; j < list.size(); j++) {
                    Route route = list.get(j);
                    JsonObject object = new JsonObject();
                    int to = route.getTo();
                    object.addProperty("price", (int)route.getEuro_price());
                    object.addProperty("duration", route.getTrip_duration());
                    object.addProperty("direct_routes", route.getTravel_data());
                    general.add(String.valueOf(to),object);
                }
                jsonToFile(general,path + "/partly/" + routeType,String.valueOf(location.getId()));
            }
        }
    }

    public static void folderForPartlyMaker(String folder, String routeType) throws IOException {
        File directory = new File(folder + "/partly/" + routeType);
        Path path = Paths.get(folder + "/partly/" + routeType);
        if (!directory.exists()) {
            Files.createDirectories(path);
        }
    }

    public static void jsonToFile(JsonObject object, String folder, String filename) {
        try (FileWriter file = new FileWriter(folder + "/" + filename + ".json")) {
            System.out.println(object.toString());
            file.write(object.toString());
            file.flush();
            //stringMaker(filename + ".json created");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void stringMaker (String input) {
        System.out.println(input);
        stream.println(input);
    }
}

