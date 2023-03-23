package visual.classes;

public class LoadType {
    boolean jsonLoad;
    boolean csvLoad;
    boolean sqlLoad;
    boolean validationLoad;

    public LoadType (boolean jsonLoad, boolean csvLoad, boolean sqlLoad, boolean validationLoad) {
        this.jsonLoad = jsonLoad;
        this.csvLoad = csvLoad;
        this.sqlLoad = sqlLoad;
        this.validationLoad = validationLoad;
    }

    public boolean isJsonLoad() {
        return jsonLoad;
    }

    public void setJsonLoad(boolean jsonLoad) {
        this.jsonLoad = jsonLoad;
    }

    public boolean isCsvLoad() {
        return csvLoad;
    }

    public void setCsvLoad(boolean csvLoad) {
        this.csvLoad = csvLoad;
    }

    public boolean isSqlLoad() {
        return sqlLoad;
    }

    public void setSqlLoad(boolean sqlLoad) {
        this.sqlLoad = sqlLoad;
    }

    public boolean isValidationLoad() {
        return validationLoad;
    }

    public void setValidationLoad(boolean validationLoad) {
        this.validationLoad = validationLoad;
    }
}
