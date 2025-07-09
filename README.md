## dateOffset.py

This script moves all the selected images and offsets the file names by a given amount. This is useful if the timezone is set incorrectly on a particular camera for a specific length of time.

When working with the actual PhenoCam archive, **ALWAYS perform a dry run first!**
This shows you the results of your command, without actually modifying any data. Append `--verbose --dry-run` to your command. And confirm the validity of the results before removing the dry-run flag. 

The basic structure of the command is as follows:
```bash
dateOffset.py [--negative] [--verbose] [--dry-run] [--overwrite] sitename startDate endDate offset
```

Where `sitename` is the name of the site you want to modify, `startDate` is the first date to modify (YYYY-MM-DD format), `endDate` is the last date you want to modify (YYYY-MM-DD format), and `offset` is the amount of time to add or subtract (HH:MM format).
To subtract time from the original timestamp, use the `--negative` flag (i.e. a camera is set to UTC, but instead needs to be UTC-8, you would use `8:00 --negative`).
It is **strongly discouraged** to use the `--overwrite` flag, as this can lead to data loss.

```bash
./dateOffset.py --verbose --dry-run webbrc 2024-10-10 2024-11-12 08:00 --negative
```

*Remember: time is based on the name of the file, NOT the timestamp in the image.*
