package com.example.sodcontrol.ui.theme;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
import android.graphics.drawable.Drawable;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;

public class JoystickView extends View {
    private final Paint bgPaint = new Paint();
    private final Paint handlePaint = new Paint();
    private final Point center = new Point();
    private final Point handle = new Point();
    private int radius;

    private Drawable topIcon, bottomIcon, leftIcon, rightIcon;
    private float topRotation = 0, bottomRotation = 0, leftRotation = 0, rightRotation = 0;
    private boolean topFlipX = false, topFlipY = false;
    private boolean bottomFlipX = false, bottomFlipY = false;
    private boolean leftFlipX = false, leftFlipY = false;
    private boolean rightFlipX = false, rightFlipY = false;

    private int iconSizeDp = 32;

    public interface JoystickListener {
        void onMove(float xPercent, float yPercent);
    }

    private JoystickListener listener;

    public JoystickView(Context context, AttributeSet attrs) {
        super(context, attrs);
        bgPaint.setColor(Color.parseColor("#161616"));
        handlePaint.setColor(Color.WHITE);
        setBackgroundColor(Color.TRANSPARENT);
    }

    public void setJoystickListener(JoystickListener listener) {
        this.listener = listener;
    }

    public void setJoystickIconsWithRotationAndFlip(
            Drawable top, float topDeg, boolean topFlipX, boolean topFlipY,
            Drawable bottom, float bottomDeg, boolean bottomFlipX, boolean bottomFlipY,
            Drawable left, float leftDeg, boolean leftFlipX, boolean leftFlipY,
            Drawable right, float rightDeg, boolean rightFlipX, boolean rightFlipY
    ) {
        this.topIcon = top;
        this.topRotation = topDeg;
        this.topFlipX = topFlipX;
        this.topFlipY = topFlipY;

        this.bottomIcon = bottom;
        this.bottomRotation = bottomDeg;
        this.bottomFlipX = bottomFlipX;
        this.bottomFlipY = bottomFlipY;

        this.leftIcon = left;
        this.leftRotation = leftDeg;
        this.leftFlipX = leftFlipX;
        this.leftFlipY = leftFlipY;

        this.rightIcon = right;
        this.rightRotation = rightDeg;
        this.rightFlipX = rightFlipX;
        this.rightFlipY = rightFlipY;

        invalidate();
    }

    private int dpToPx(int dp) {
        return (int) (dp * getResources().getDisplayMetrics().density);
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

        drawIcons(canvas);

        canvas.drawCircle(handle.x, handle.y, 40, handlePaint);
    }


    private void drawIcons(Canvas canvas) {
        float scale = 0.08f;
        float offset = radius * 0.8f;

        drawIcon(canvas, topIcon, center.x, center.y - (int) offset, topRotation, topFlipX, topFlipY, scale);
        drawIcon(canvas, bottomIcon, center.x, center.y + (int) offset, bottomRotation, bottomFlipX, bottomFlipY, scale);
        drawIcon(canvas, leftIcon, center.x - (int) offset, center.y, leftRotation, leftFlipX, leftFlipY, scale);
        drawIcon(canvas, rightIcon, center.x + (int) offset, center.y, rightRotation, rightFlipX, rightFlipY, scale);
    }



    private void drawIcon(Canvas canvas, Drawable icon, int cx, int cy, float rotation, boolean flipX, boolean flipY, float scale) {
        if (icon == null) return;

        canvas.save();

        canvas.translate(cx, cy);

        canvas.rotate(rotation);

        canvas.scale((flipX ? -1f : 1f) * scale, (flipY ? -1f : 1f) * scale);

        int halfW = icon.getIntrinsicWidth() / 2;
        int halfH = icon.getIntrinsicHeight() / 2;
        icon.setBounds(-halfW, -halfH, halfW, halfH);

        icon.draw(canvas);
        canvas.restore();
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
