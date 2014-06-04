package test.teamcity.testModule1;

import android.content.Context;
import android.os.Handler;
import android.os.Looper;
import android.widget.Toast;

/**
 * Created by kunjanagarwal on 6/4/14.
 */
public class ToastMaker {

    public static void showToast(final Context context, final String toast){
        new Handler(Looper.getMainLooper()).post(new Runnable()
        {
            @Override
            public void run()
            {
                Toast.makeText(context, toast, Toast.LENGTH_LONG).show();
            }
        });
    }
}
