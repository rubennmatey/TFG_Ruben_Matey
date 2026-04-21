from app.services.system_service import AccessControlSystem


def main():
    system = AccessControlSystem()
    system.run()


if __name__ == "__main__":
    main()