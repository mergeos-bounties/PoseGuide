import torch
import torch.nn as nn

class PoseEncoder(nn.Module):
    def __init__(self, input_dim=66, hidden_dim=128, embed_dim=64):
        # input_dim=66 for 33 2D mediapipe landmarks
        super(PoseEncoder, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, embed_dim)
        )
        
    def forward(self, x):
        return self.net(x)

class SiamesePoseSimilarity(nn.Module):
    def __init__(self, encoder):
        super(SiamesePoseSimilarity, self).__init__()
        self.encoder = encoder
        
    def forward(self, pose1, pose2):
        embed1 = self.encoder(pose1)
        embed2 = self.encoder(pose2)
        # Cosine similarity for distance
        return nn.functional.cosine_similarity(embed1, embed2, dim=-1)

def contrastive_loss(similarity, label, margin=0.5):
    """
    label: 1 if similar, -1 if dissimilar
    """
    loss_similar = torch.mean((1 - similarity)[label == 1]**2)
    loss_dissimilar = torch.mean(torch.clamp(similarity - margin, min=0)[label == -1]**2)
    return loss_similar + loss_dissimilar

if __name__ == "__main__":
    encoder = PoseEncoder()
    model = SiamesePoseSimilarity(encoder)
    
    # Dummy batched inputs
    pose_a = torch.randn(4, 66)
    pose_b = torch.randn(4, 66)
    sim = model(pose_a, pose_b)
    print(f"Similarity output shape: {sim.shape}")
    print("Siamese baseline initialized.")