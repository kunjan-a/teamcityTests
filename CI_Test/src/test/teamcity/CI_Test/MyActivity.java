package test.teamcity.CI_Test;

import android.app.Activity;
import android.os.Bundle;
import test.teamcity.testModule1.ToastMaker;

public class MyActivity extends Activity {
    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        ToastMaker.showToast(getApplicationContext(), "Welcome ");
    }
}
