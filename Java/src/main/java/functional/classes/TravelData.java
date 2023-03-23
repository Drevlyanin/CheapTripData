package functional.classes;

import java.util.Comparator;

public class TravelData implements Comparable<TravelData> {
    private int id;
    private int from;
    private int to;
    private int transportation_type;
    private float euro_price;
    private int time_in_minutes;

    public TravelData(int id, int from, int to, int transportation_type, float euro_price, int time_in_minutes) {
        this.id = id;
        this.from = from;
        this.to = to;
        this.transportation_type = transportation_type;
        this.euro_price = euro_price;
        this.time_in_minutes = time_in_minutes;
    }

    public TravelData(int from, int to, int transportation_type, float euro_price, int time_in_minutes) {
        this.from = from;
        this.to = to;
        this.transportation_type = transportation_type;
        this.euro_price = euro_price;
        this.time_in_minutes = time_in_minutes;
    }

    public TravelData() {
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getFrom() {
        return from;
    }

    public void setFrom(int from) {
        this.from = from;
    }

    public int getTo() {
        return to;
    }

    public void setTo(int to) {
        this.to = to;
    }

    public int getTransportation_type() {
        return transportation_type;
    }

    public void setTransportation_type(int transportation_type) {
        this.transportation_type = transportation_type;
    }

    public float getEuro_price() {
        return euro_price;
    }

    public void setEuro_price(float euro_price) {
        this.euro_price = euro_price;
    }

    public int getTime_in_minutes() {
        return time_in_minutes;
    }

    public void setTime_in_minutes(int time_in_minutes) {
        this.time_in_minutes = time_in_minutes;
    }

    @Override
    public String toString() {
        return "id=" + id +
                ", from=" + from +
                ", to=" + to +
                ", transportation_type=" + transportation_type +
                ", euro_price=" + euro_price +
                ", time_in_minutes=" + time_in_minutes;
    }

    public String getName() {
        return "" + id;
    }

    @Override
    public int compareTo(TravelData o) {
        return Comparator.comparing(TravelData::getFrom)
                .thenComparing(TravelData::getTo)
                .thenComparing(TravelData::getEuro_price).compare(this, o);
    }
}
