package com.example.sodcontrol.ui.theme;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;

public class JoystickView extends View {
    private final Paint bgPaint = new Paint();
    private final Paint handlePaint = new Paint();
    private final Point center = new Point();
    private final Point handle = new Point();
    private int radius;

    public interface JoystickListener {
        void onMove(float xPercent, float yPercent);
    }

    private JoystickListener listener;

    public JoystickView(Context context, AttributeSet attrs) {
        super(context, attrs);
        bgPaint.setColor(Color.GRAY);
        handlePaint.setColor(Color.BLUE);
        setBackgroundColor(Color.TRANSPARENT);
    }

    public void setJoystickListener(JoystickListener listener) {
        this.listener = listener;
    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        radius = Math.min(w, h) / 2 - 20;
        center.set(w / 2, h / 2);
        handle.set(center.x, center.y);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        canvas.drawCircle(center.x, center.y, radius, bgPaint);
        canvas.drawCircle(handle.x, handle.y, 40, handlePaint);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        float dx = event.getX() - center.x;
        float dy = event.getY() - center.y;
        float distance = (float) Math.sqrt(dx * dx + dy * dy);

        if (distance < radius) {
            handle.set((int) event.getX(), (int) event.getY());
        } else {
            float ratio = radius / distance;
            handle.set((int) (center.x + dx * ratio), (int) (center.y + dy * ratio));
        }

        invalidate();

        if (listener != null) {
            float xPercent = (handle.x - center.x) / (float) radius;
            float yPercent = (handle.y - center.y) / (float) radius;
            listener.onMove(xPercent, yPercent);
        }

        if (event.getAction() == MotionEvent.ACTION_UP) {
            handle.set(center.x, center.y);
            invalidate();
            if (listener != null) listener.onMove(0, 0);
        }

        return true;
    }
}
