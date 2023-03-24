package functional.classes;

public class TravelDataValidationStatus {
    private int id;
    private int from;
    private int to;
    private int transportation_type;
    private float euro_price;
    private int time_in_minutes;
    private int counter;
    private String alternatePath;
    private float alternatePrice;
    private float status;

    public TravelDataValidationStatus(int id, int from, int to, int transportation_type, float euro_price,
                                      int time_in_minutes, int counter, String alternatePath, float alternatePrice,
                                      float status) {
        this.id = id;
        this.from = from;
        this.to = to;
        this.transportation_type = transportation_type;
        this.euro_price = euro_price;
        this.time_in_minutes = time_in_minutes;
        this.counter = counter;
        this.alternatePath = alternatePath;
        this.alternatePrice = alternatePrice;
        this.status = status;
    }

    public TravelDataValidationStatus() {
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

    public int getCounter() {
        return counter;
    }

    public void setCounter(int counter) {
        this.counter = counter;
    }

    public String getAlternatePath() {
        return alternatePath;
    }

    public void setAlternatePath(String alternatePath) {
        this.alternatePath = alternatePath;
    }

    public float getAlternatePrice() {
        return alternatePrice;
    }

    public void setAlternatePrice(float alternatePrice) {
        this.alternatePrice = alternatePrice;
    }

    public float getStatus() {
        return status;
    }

    public void setStatus(float status) {
        this.status = status;
    }

    @Override
    public String toString() {
        return "TravelDataValidationStatus{" +
                "id=" + id +
                ", from=" + from +
                ", to=" + to +
                ", transportation_type=" + transportation_type +
                ", euro_price=" + euro_price +
                ", time_in_minutes=" + time_in_minutes +
                ", counter=" + counter +
                ", alternatePath='" + alternatePath + '\'' +
                ", alternatePrice=" + alternatePrice +
                ", status=" + status +
                '}';
    }
}
