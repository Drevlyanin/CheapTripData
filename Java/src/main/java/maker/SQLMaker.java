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
import java.util.List;

public class SQLMaker {

    public static Console console = MenuInitializer.console;
    public static PrintStream stream = new PrintStream(console);

    public static String locationsToString(List<Location> locations) {
        String result = "INSERT INTO locations (id, name, latitude, longitude) VALUES ";
        for (int i = 0; i < locations.size(); i++) {
            Location location = locations.get(i);
            result = result + "(" + location.getId() + ",'" +
                    location.getName() + "'," +
                    location.getLatitude() + "," +
                    location.getLongitude() + ")";
            if (i < locations.size() - 1) {
                result = result + ",\n";
            } else {
                result = result + ";\n";
            }
        }
        return result;
    }

    public static void locationsSQL(String input, String folder) {
        String result = "DROP TABLE IF EXISTS locations;" + "\n" +
                "CREATE TABLE locations " + "\n" +
                "(" + "\n" +
                "   id                  INT                 NOT NULL," + "\n" +
                "   name                VARCHAR(40)         NOT NULL," + "\n" +
                "   latitude            DECIMAL(12, 2)      NOT NULL," + "\n" +
                "   longitude           DECIMAL(12, 2)      NOT NULL," + "\n" +
                "PRIMARY KEY (id)" + "\n" +
                ") ENGINE = InnoDB" + "\n" +
                "DEFAULT CHARSET = utf8;" + "\n" +
                "LOCK TABLES locations WRITE;" + "\n" +
                input + "\n" +
                "UNLOCK TABLES;";
        sqlToFile(result, folder + "/locations.sql");
        stringMaker("locations.sql created");
    }

    public static String transportationTypesToString(List<TransportationType> types) {
        String result = "INSERT INTO transportation_types (id, name) VALUES ";
        for (int i = 0; i < types.size(); i++) {
            TransportationType type = types.get(i);
            result = result + "(" + type.getId() + ",'" +
                    type.getName() + "')";
            if (i < types.size() - 1) {
                result = result + ",\n";
            } else {
                result = result + ";\n";
            }
        }
        return result;
    }

    public static void transportationTypesSQL(String input, String folder) {
        String result = "DROP TABLE IF EXISTS transportation_types;" + "\n" +
                "CREATE TABLE transportation_types " + "\n" +
                "(" + "\n" +
                "   id                  INT                 NOT NULL," + "\n" +
                "   name                VARCHAR(30)         NOT NULL," + "\n" +
                "PRIMARY KEY (id)" + "\n" +
                ") ENGINE = InnoDB" + "\n" +
                "DEFAULT CHARSET = utf8;" + "\n" +
                "LOCK TABLES transportation_types WRITE;" + "\n" +
                input + "\n" +
                "UNLOCK TABLES;";
        sqlToFile(result, folder + "/transportation_types.sql");
        stringMaker("transportation_types.sql created");
    }

    public static String routesToString(List<Route> routes, String routeTable) {
        String result = "INSERT INTO " + routeTable + " (id, `from`,`to`, euro_price, trip_duration, travel_data) " +
                "VALUES ";
        for (int i = 0; i < routes.size(); i++) {
            Route route = routes.get(i);
            result = result + "(" + route.getId() + "," +
                    route.getFrom() + "," +
                    route.getTo() + "," +
                    route.getEuro_price() + "," +
                    route.getTrip_duration() + ",'" +
                    route.getTravel_data() + "')";
            if (i < routes.size() - 1) {
                result = result + ",\n";
            } else {
                result = result + ";\n";
            }
        }
        return result;
    }

    public static void routesSQL(String input, String routeTable, String folder) {
        String result = "DROP TABLE IF EXISTS " + routeTable + ";" + "\n" +
                "CREATE TABLE " + routeTable + "\n" +
                "(" + "\n" +
                "   id                  INT                 NOT NULL," + "\n" +
                "   `from`              INT                 NOT NULL," + "\n" +
                "   `to`                INT                 NOT NULL," + "\n" +
                "   euro_price          FLOAT               NOT NULL," + "\n" +
                "   trip_duration       INT                 NOT NULL," + "\n" +
                "   travel_data         VARCHAR(255)        NOT NULL," + "\n" +
                "PRIMARY KEY (id)" + "\n" +
                ") ENGINE = InnoDB" + "\n" +
                "DEFAULT CHARSET = utf8;" + "\n" +
                "LOCK TABLES " + routeTable + " WRITE;" + "\n" +
                input + "\n" +
                "UNLOCK TABLES;";
        sqlToFile(result, folder + "/" + routeTable + ".sql");
        stringMaker(routeTable + ".sql created");
    }

    public static String travelDataToString(List<TravelData> datas) {
        String result = "INSERT INTO travel_data (id, `from`,`to`, transportation_type, euro_price, time_in_minutes) " +
                "VALUES ";
        for (int i = 0; i < datas.size(); i++) {
            TravelData data = datas.get(i);
            result = result + "(" + data.getId() + "," +
                    data.getFrom() + "," +
                    data.getTo() + "," +
                    data.getTransportation_type() + "," +
                    data.getEuro_price() + "," +
                    data.getTime_in_minutes() + ")";
            if (i < datas.size() - 1) {
                result = result + ",\n";
            } else {
                result = result + ";\n";
            }
        }
        return result;
    }

    public static void travelDataSQL(String input, String path) {
        String result = "DROP TABLE IF EXISTS travel_data;" + "\n" +
                "CREATE TABLE travel_data" + "\n" +
                "(" + "\n" +
                "   id                  INT                 NOT NULL," + "\n" +
                "   `from`              INT                 NOT NULL," + "\n" +
                "   `to`                INT                 NOT NULL," + "\n" +
                "   transportation_type INT                 NOT NULL," + "\n" +
                "   euro_price          FLOAT               NOT NULL," + "\n" +
                "   time_in_minutes     INT                 NOT NULL," + "\n" +
                "PRIMARY KEY (id)" + "\n" +
                ") ENGINE = InnoDB" + "\n" +
                "DEFAULT CHARSET = utf8;" + "\n" +
                "LOCK TABLES travel_data WRITE;" + "\n" +
                input + "\n" +
                "UNLOCK TABLES;";
        sqlToFile(result, path + "/travel_data.sql");
        stringMaker("travel_data.sql created");
    }

    public static void sqlToFile(String input, String filename) {
        try (FileWriter file = new FileWriter(filename)) {
            file.write(input);
            file.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void stringMaker (String input) {
        System.out.println(input);
        stream.println(input);
    }
}
