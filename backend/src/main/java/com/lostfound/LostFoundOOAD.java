package com.lostfound;

import java.util.ArrayList;
import java.util.List;

// ABSTRACTION + ENCAPSULATION
abstract class CampusUser {

    private int userId;
    private String name;
    private String email;

    public CampusUser(int userId, String name, String email) {
        this.userId = userId;
        this.name = name;
        this.email = email;
    }

    public int getUserId() {
        return userId;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    // POLYMORPHISM
    public abstract void displayRole();
}


// INHERITANCE
class Student extends CampusUser {

    public Student(int id, String name, String email) {
        super(id, name, email);
    }

    @Override
    public void displayRole() {
        System.out.println("Role: Student");
    }

    public void reportItem(Item item) {
        System.out.println(
            getName() + " reported " + item.getName()
        );
    }
}


// INHERITANCE
class Admin extends CampusUser {

    public Admin(int id, String name, String email) {
        super(id, name, email);
    }

    @Override
    public void displayRole() {
        System.out.println("Role: Administrator");
    }

    public void verifyClaim(Claim claim, boolean approved) {

        if (approved) {
            claim.setStatus("Approved");
            claim.getItem().setStatus("Recovered");
        } else {
            claim.setStatus("Rejected");
        }
    }
}


// ITEM CLASS
class Item {

    private int itemId;
    private String name;
    private String category;
    private String location;
    private String type;
    private String status;

    public Item(
            int itemId,
            String name,
            String category,
            String location,
            String type) {

        this.itemId = itemId;
        this.name = name;
        this.category = category;
        this.location = location;
        this.type = type;

        if (type.equalsIgnoreCase("Lost")) {
            this.status = "Searching";
        } else {
            this.status = "Available";
        }
    }

    public int getItemId() {
        return itemId;
    }

    public String getName() {
        return name;
    }

    public String getCategory() {
        return category;
    }

    public String getLocation() {
        return location;
    }

    public String getType() {
        return type;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public void displayItem() {
        System.out.println(
            name + " | " +
            category + " | " +
            location + " | " +
            status
        );
    }
}


// CLAIM CLASS
class Claim {

    private int claimId;
    private Item item;
    private CampusUser claimant;
    private String proof;
    private String status;

    public Claim(
            int claimId,
            Item item,
            CampusUser claimant,
            String proof) {

        this.claimId = claimId;
        this.item = item;
        this.claimant = claimant;
        this.proof = proof;
        this.status = "Pending";
    }

    public int getClaimId() {
        return claimId;
    }

    public Item getItem() {
        return item;
    }

    public CampusUser getClaimant() {
        return claimant;
    }

    public String getProof() {
        return proof;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}


// NOTIFICATION CLASS
class Notification {

    private CampusUser receiver;
    private String message;

    public Notification(
            CampusUser receiver,
            String message) {

        this.receiver = receiver;
        this.message = message;
    }

    public void send() {
        System.out.println(
            "Notification to " +
            receiver.getName() +
            ": " +
            message
        );
    }
}


// MATCHING SERVICE
class MatchingService {

    public int calculateMatch(Item lost, Item found) {

        int score = 0;

        if (lost.getCategory()
                .equalsIgnoreCase(found.getCategory())) {
            score += 40;
        }

        if (lost.getLocation()
                .equalsIgnoreCase(found.getLocation())) {
            score += 30;
        }

        if (lost.getName()
                .equalsIgnoreCase(found.getName())) {
            score += 30;
        }

        return score;
    }
}


// MAIN SYSTEM
public class LostFoundOOAD {

    public static void main(String[] args) {

        System.out.println(
            "=== SMART LOST & FOUND CAMPUS SYSTEM ==="
        );

        // OBJECTS
        Student student = new Student(
            1,
            "Student User",
            "student@campus.edu"
        );

        Admin admin = new Admin(
            2,
            "System Admin",
            "admin@campus.edu"
        );

        // POLYMORPHISM
        CampusUser user1 = student;
        CampusUser user2 = admin;

        user1.displayRole();
        user2.displayRole();

        // LOST ITEM
        Item lostPhone = new Item(
            101,
            "Samsung Phone",
            "Electronics",
            "Cafeteria",
            "Lost"
        );

        // FOUND ITEM
        Item foundPhone = new Item(
            102,
            "Samsung Phone",
            "Electronics",
            "Cafeteria",
            "Found"
        );

        // COLLECTION
        List<Item> items = new ArrayList<>();

        items.add(lostPhone);
        items.add(foundPhone);

        student.reportItem(lostPhone);

        System.out.println("\n--- Item Reports ---");

        for (Item item : items) {
            item.displayItem();
        }

        // MATCHING
        MatchingService matcher =
            new MatchingService();

        int score = matcher.calculateMatch(
            lostPhone,
            foundPhone
        );

        System.out.println(
            "\nPossible Match Score: " +
            score + "%"
        );

        // CLAIM
        Claim claim = new Claim(
            501,
            foundPhone,
            student,
            "Can identify lock screen and phone cover"
        );

        System.out.println(
            "Claim Status: " +
            claim.getStatus()
        );

        // ADMIN VERIFICATION
        admin.verifyClaim(claim, true);

        System.out.println(
            "Claim Status after verification: " +
            claim.getStatus()
        );

        System.out.println(
            "Item Status: " +
            foundPhone.getStatus()
        );

        // NOTIFICATION
        Notification notification =
            new Notification(
                student,
                "Your claim has been approved."
            );

        notification.send();

        System.out.println(
            "\n=== RECOVERY PROCESS COMPLETED ==="
        );
    }
}