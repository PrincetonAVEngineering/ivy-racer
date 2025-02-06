using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarControlling : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }
    // Update is called once per frame
    public float speed = 10f;
    public float turnSpeed = 50f;

    private void Update()
    {
        float moveDirection = Input.GetAxis("Vertical"); // W/S keys or Up/Down arrow
        float turnDirection = Input.GetAxis("Horizontal"); // A/D keys or Left/Right arrow

        // Move the car forward and backward
        transform.Translate(Vector3.forward * moveDirection * speed * Time.deltaTime);

        // Rotate the car left and right
        transform.Rotate(Vector3.up, turnDirection * turnSpeed * Time.deltaTime);
    }
}
