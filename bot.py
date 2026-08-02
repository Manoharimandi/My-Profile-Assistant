if __name__ == '__main__':
    # 🚀 THE FINAL 2-LINE FIX: Prevent Render from marking it as failed when the second instance exits
    render_instance_id = os.environ.get("RENDER_INSTANCE_ID", "0")
    
    # Only Instance 0 runs the actual bot.
    if render_instance_id == "0":
        try:
            print("🚀 Primary instance detected. Starting bot...")
            asyncio.run(main())
        except KeyboardInterrupt:
            pass
        except RuntimeError as e:
            if "Event loop is closed" in str(e):
                pass
            else:
                raise e
            
    else:
        # Instance 1, 2, etc. simply print a message and EXIT NORMALLY (status code 0).
        print(f"👋 Secondary instance ({render_instance_id}) detected. Shutting down silently to prevent conflicts.")
        # Exiting with 0 tells Render "This task finished successfully, no errors."
        sys.exit(0)
