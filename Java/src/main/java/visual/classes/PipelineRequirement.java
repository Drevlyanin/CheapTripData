package visual.classes;

public class PipelineRequirement {
    boolean isRequired;

    public PipelineRequirement(boolean isRequired) {
        this.isRequired = isRequired;
    }

    public boolean isRequired() {
        return isRequired;
    }

    public void setRequired(boolean required) {
        isRequired = required;
    }
}
