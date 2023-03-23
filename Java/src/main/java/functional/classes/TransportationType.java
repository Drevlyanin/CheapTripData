package functional.classes;

public class TransportationType {
    public int id;
    public String name;

    public TransportationType(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public TransportationType(){}

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String toString() {
        return "id=" + id +
                ", name='" + name;
    }
}
