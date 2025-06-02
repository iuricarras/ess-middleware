# Hypervisor Cluster HA & LM Manager - Daemon

**⚠️ Warning:** This code is an academic project and is not intended for production use.

This daemon is a Python service that manages high-availability (HA) and live migration (LM) for Proxmox clusters. It acts as a bridge between the web platform ([frontend](https://github.com/rodrigo-gom3s/ess-frontend) and [backend](https://github.com/iuricarras/ess-backend)) and the Proxmox cluster, enabling fault tolerance management, live migration, and HA group/resource control.

## Main Functionalities

- **Proxmox Cluster Integration:** Connects to Proxmox clusters to monitor nodes and VMs.
- **Fault Tolerance:** Automatically manages VM snapshots and initiates recovery/migration if a node goes offline.
- **HA Groups & Resources:** Create, delete, and manage Proxmox HA groups and resources.
- **Remote Migration:** Supports remote VM migration between nodes and storage backends.
- **WebSocket API:** Real-time communication with frontend and backend services.
- **Database Integration:** Tracks managed VMs using SQLite.

## Installation Guide

### Prerequisites

- Python 3.12+
- [Proxmox cluster](https://www.proxmox.com/proxmox-ve)
- python3-virtualenv package (install with `sudo apt install python3-virtualenv` on Debian/Ubuntu)
- pip (comes bundled with recent Python versions)
- [Nix](https://nixos.org/download.html) (optional, for reproducible environments)

### 1. Clone the Repository

```sh
git clone https://github.com/iuricarras/ess-middleware.git
cd ess-middleware
```

### 2. Install Dependencies

#### Using venv (recommended)

Create and activate a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
```

Install all dependencies:

```sh
pip install -r requirements.txt
```

#### Using Nix (Opcional)

```sh
nix-shell
```


### 3. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
PROXMOX_IP=your-proxmox-ip
PROXMOX_PORT=your-proxmox-port
PROXMOX_USER=your-proxmox-user
PROXMOX_PASSWORD=your-proxmox-password
PUSHOVER_TOKEN=your-pushover-token
PUSHOVER_USER=your-pushover-user
```

### 4. Run the Middleware

```sh
python -m package
```

## Related Repositories

- **Frontend:** [rodrigo-gom3s/ess-frontend](https://github.com/rodrigo-gom3s/ess-frontend)
- **Backend:** [iuricarras/ess-backend](https://github.com/iuricarras/ess-backend)

## License

This project is licensed under the MIT License.
