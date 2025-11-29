
def write_replay_fdr(df, path):
    """ Custom .fdr file format """

    with open(path, "w") as f:
        f.write("\n".join([
            "A",
            "1000 Version",
            "FDR Created by Flight Data Replay Project",
            "I",
            "Time,Longitude,Latitude,Altitude,Roll,Pitch,Yaw",
            "DATA"
        ]) + "\n")
        
        df_export = df.rename(columns={
            "Roll (deg)": "Roll",
            "Pitch (deg)": "Pitch", 
            "Yaw (deg)": "Yaw"
        })

        for row in df_export.itertuples():
            f.write(
                f"{row.Time:.3f},{row.Longitude:.6f},{row.Latitude:.6f},"
                f"{row.Altitude:.2f},{row.Roll:.2f},{row.Pitch:.2f},{row.Yaw:.2f}\n"
            )