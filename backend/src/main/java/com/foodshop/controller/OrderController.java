package com.foodshop.controller;

import com.foodshop.dto.OrderItemRequest;
import com.foodshop.dto.OrderRequest;
import com.foodshop.model.Order;
import com.foodshop.model.OrderItem;
import com.foodshop.model.User;
import com.foodshop.repository.OrderRepository;
import com.foodshop.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/orders")
@CrossOrigin(origins = "*")
public class OrderController {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private UserRepository userRepository;

    @PostMapping
    public ResponseEntity<?> createOrder(@RequestBody OrderRequest request) {
        try {
            Order order = new Order();
            
            if (request.getUserId() != null) {
                Optional<User> userOpt = userRepository.findById(request.getUserId());
                if (userOpt.isPresent()) {
                    order.setUser(userOpt.get());
                }
            }

            order.setCustomerName(request.getCustomerName());
            order.setCustomerPhone(request.getCustomerPhone());
            order.setDeliveryAddress(request.getDeliveryAddress());
            order.setPaymentMethod(request.getPaymentMethod());
            order.setTotalAmount(request.getTotalAmount());
            order.setOrderDate(LocalDateTime.now());
            order.setStatus("PENDING");

            for (OrderItemRequest itemReq : request.getItems()) {
                OrderItem item = new OrderItem();
                item.setFoodName(itemReq.getFoodName());
                item.setPrice(itemReq.getPrice());
                item.setQuantity(itemReq.getQuantity());
                order.addItem(item);
            }

            Order savedOrder = orderRepository.save(order);
            return ResponseEntity.ok(savedOrder);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Error placing order: " + e.getMessage());
        }
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<?> getUserOrders(@PathVariable Long userId) {
        try {
            List<Order> orders = orderRepository.findByUserIdOrderByOrderDateDesc(userId);
            return ResponseEntity.ok(orders);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Error fetching orders: " + e.getMessage());
        }
    }

    @GetMapping("/registered")
    public ResponseEntity<?> getRegisteredUserOrders() {
        try {
            List<Order> orders = orderRepository.findByUserIdIsNotNullOrderByOrderDateDesc();
            return ResponseEntity.ok(orders);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Error fetching registered user orders: " + e.getMessage());
        }
    }

    @GetMapping("/all")
    public ResponseEntity<?> getAllOrders() {
        try {
            List<Order> orders = orderRepository.findAllByOrderByOrderDateDesc();
            return ResponseEntity.ok(orders);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Error fetching all orders: " + e.getMessage());
        }
    }

    @PutMapping("/{id}/status")
    public ResponseEntity<?> updateOrderStatus(@PathVariable Long id, @RequestBody java.util.Map<String, String> body) {
        try {
            Optional<Order> orderOpt = orderRepository.findById(id);
            if (orderOpt.isPresent()) {
                Order order = orderOpt.get();
                order.setStatus(body.get("status"));
                orderRepository.save(order);
                return ResponseEntity.ok(order);
            }
            return ResponseEntity.notFound().build();
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Error updating status: " + e.getMessage());
        }
    }
}
