from services.card_generator import generate_gratitude_card


output = generate_gratitude_card (
    card_id =1,
    message = "Thank you for excellent contribution and continous support to the team. Your dedication truly makes a difference.",
    sender_name="Shivani",
    receiver_name="AI TEST",
    output_filename="test_card.png"
)

print("Generated card at: ", output)