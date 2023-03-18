package functional.classes;

import java.util.Comparator;

public class CounterFeature implements Comparable<CounterFeature> {

    private int id;
    private int count;

    public CounterFeature(int id, int count) {
        this.id = id;
        this.count = count;
    }

    public CounterFeature() {
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getCount() {
        return count;
    }

    public void setCount(int count) {
        this.count = count;
    }

    @Override
    public int compareTo(CounterFeature feature) {
        return Comparator.comparing(CounterFeature::getCount)
                .reversed()
                .thenComparing(CounterFeature::getCount).compare(this, feature);
    }
}
