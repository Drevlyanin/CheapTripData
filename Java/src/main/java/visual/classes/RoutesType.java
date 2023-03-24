package visual.classes;

public class RoutesType {
    boolean routesDefault;
    boolean fixedRoutesDefault;
    boolean flyingRoutesDefault;

    public RoutesType (boolean routesDefault, boolean fixedRoutesDefault, boolean flyingRoutesDefault) {
        this.routesDefault = routesDefault;
        this.fixedRoutesDefault = fixedRoutesDefault;
        this.flyingRoutesDefault = flyingRoutesDefault;
    }

    public boolean isRoutesDefault() {
        return routesDefault;
    }

    public void setRoutesDefault(boolean routesDefault) {
        this.routesDefault = routesDefault;
    }

    public boolean isFixedRoutesDefault() {
        return fixedRoutesDefault;
    }

    public void setFixedRoutesDefault(boolean fixedRoutesDefault) {
        this.fixedRoutesDefault = fixedRoutesDefault;
    }

    public boolean isFlyingRoutesDefault() {
        return flyingRoutesDefault;
    }

    public void setFlyingRoutesDefault(boolean flyingRoutesDefault) {
        this.flyingRoutesDefault = flyingRoutesDefault;
    }
}
