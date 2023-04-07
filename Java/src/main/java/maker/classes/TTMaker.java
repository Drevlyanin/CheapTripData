package maker.classes;

import functional.classes.TransportationType;

import java.util.ArrayList;

public class TTMaker {

    public static ArrayList<TransportationType> typesInitializer() {
        ArrayList<TransportationType> result = new ArrayList<>();
        result.add(new TransportationType(1, "Flight"));
        result.add(new TransportationType(2, "Bus"));
        result.add(new TransportationType(3, "Train"));
        result.add(new TransportationType(4, "Car Drive"));
        result.add(new TransportationType(5, "Taxi"));
        result.add(new TransportationType(6, "Walk"));
        result.add(new TransportationType(7, "Town Car"));
        result.add(new TransportationType(8, "Ride Share"));
        result.add(new TransportationType(9, "Shuttle"));
        result.add(new TransportationType(10, "Ferry"));
        result.add(new TransportationType(11, "Subway"));
        return result;
    }
}
